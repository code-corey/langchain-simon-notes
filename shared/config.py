"""
项目级配置与模型工厂。

从仓库根目录的 .env 读取密钥与模型名，对外提供统一的
聊天模型 / Embedding 创建入口。支持聊天与向量服务分离部署
（例如 llama.cpp 聊天 + xinference embedding）。
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# 仓库根目录（shared 的上一级）
REPO_ROOT = Path(__file__).resolve().parent.parent


@dataclass(frozen=True)
class Settings:
    """运行时配置快照。"""

    openai_api_key: str
    openai_base_url: str | None
    model_name: str
    embedding_base_url: str | None
    embedding_model: str
    has_api_key: bool


def normalize_openai_base_url(url: str | None) -> str | None:
    """
    规范化 OpenAI Compatible Base URL。

    去掉末尾斜杠；若未以 /v1 结尾则自动补上，避免漏写路径。

    :param url: 原始地址，可为 None。
    :return: 规范化后的地址，或 None。
    """
    if not url:
        return None
    cleaned = url.strip().rstrip("/")
    if not cleaned:
        return None
    if cleaned.endswith("/v1"):
        return cleaned
    return f"{cleaned}/v1"


def load_settings(*, require_api_key: bool = True) -> Settings:
    """
    加载 .env 并组装 Settings。

    :param require_api_key: 为 True 时若缺少密钥则直接退出并提示。
    :return: 配置快照。
    """
    load_dotenv(REPO_ROOT / ".env")
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    # 本地 OpenAI Compatible 常不校验 Key，允许用占位值
    if not api_key:
        api_key = "local"

    base_url = normalize_openai_base_url(
        (os.getenv("OPENAI_BASE_URL") or "").strip() or None
    )
    model_name = (os.getenv("MODEL_NAME") or "openai:gpt-4o-mini").strip()

    embedding_base_url = normalize_openai_base_url(
        (os.getenv("EMBEDDING_BASE_URL") or "").strip() or None
    )
    # 未单独配置时，回退到聊天网关（同一服务既聊天又 embedding 的场景）
    if embedding_base_url is None:
        embedding_base_url = base_url

    embedding_model = (
        os.getenv("EMBEDDING_MODEL") or "text-embedding-3-small"
    ).strip()

    has_real_key = bool((os.getenv("OPENAI_API_KEY") or "").strip())
    if require_api_key and not has_real_key and base_url is None:
        print(
            "未检测到 OPENAI_API_KEY，且未配置 OPENAI_BASE_URL。\n"
            "请复制 .env.example 为 .env：云端填密钥，局域网填 Base URL（Key 可用 local）。",
            file=sys.stderr,
        )
        sys.exit(1)

    return Settings(
        openai_api_key=api_key,
        openai_base_url=base_url,
        model_name=model_name,
        embedding_base_url=embedding_base_url,
        embedding_model=embedding_model,
        has_api_key=has_real_key or bool(base_url),
    )


def print_settings_summary(settings: Settings) -> None:
    """
    打印脱敏后的配置摘要，便于排障。

    :param settings: 配置快照。
    """
    raw_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if raw_key and len(raw_key) > 10:
        key_preview = f"{raw_key[:6]}...{raw_key[-4:]}"
    elif raw_key:
        key_preview = raw_key
    else:
        key_preview = "local（占位）"

    print("=== 运行配置 ===")
    print(f"MODEL_NAME         : {settings.model_name}")
    print(f"OPENAI_BASE_URL    : {settings.openai_base_url or '(默认官方)'}")
    print(f"EMBEDDING_MODEL    : {settings.embedding_model}")
    print(f"EMBEDDING_BASE_URL : {settings.embedding_base_url or '(同聊天网关/官方)'}")
    print(f"OPENAI_API_KEY     : {key_preview}")


def get_chat_model(*, temperature: float = 0.2):
    """
    使用 init_chat_model 创建聊天模型。

    若配置了自定义 Base URL，则使用 ChatOpenAI 对接 OpenAI Compatible 网关
    （如 llama.cpp、vLLM、OneAPI 等）。

    :param temperature: 采样温度。
    :return: 可 invoke / stream 的聊天模型实例。
    """
    settings = load_settings(require_api_key=True)

    if settings.openai_base_url:
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=_strip_provider_prefix(settings.model_name),
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            temperature=temperature,
        )

    from langchain.chat_models import init_chat_model

    return init_chat_model(
        settings.model_name,
        temperature=temperature,
        api_key=settings.openai_api_key,
    )


def get_embeddings():
    """
    创建 Embedding 模型，供 RAG 向量化使用。

    优先使用独立的 EMBEDDING_BASE_URL（可与聊天服务分离）。

    :return: Embeddings 实例。
    """
    settings = load_settings(require_api_key=True)
    from langchain_openai import OpenAIEmbeddings

    kwargs: dict = {
        "model": settings.embedding_model,
        "api_key": settings.openai_api_key,
    }
    if settings.embedding_base_url:
        kwargs["base_url"] = settings.embedding_base_url
    return OpenAIEmbeddings(**kwargs)


def _strip_provider_prefix(model_name: str) -> str:
    """
    去掉 init_chat_model 风格的 provider 前缀，例如 openai:gpt-4o-mini。

    :param model_name: 原始模型名。
    :return: 纯模型名。
    """
    if ":" in model_name:
        return model_name.split(":", 1)[1]
    return model_name
