"""
项目级配置与模型工厂。

从仓库根目录的 .env 读取密钥与模型名，对外提供统一的
聊天模型 / Embedding 创建入口，保证 8 个模块行为一致。
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
    embedding_model: str
    has_api_key: bool


def load_settings(*, require_api_key: bool = True) -> Settings:
    """
    加载 .env 并组装 Settings。

    :param require_api_key: 为 True 时若缺少密钥则直接退出并提示。
    :return: 配置快照。
    """
    load_dotenv(REPO_ROOT / ".env")
    api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
    base_url = (os.getenv("OPENAI_BASE_URL") or "").strip() or None
    model_name = (os.getenv("MODEL_NAME") or "openai:gpt-4o-mini").strip()
    embedding_model = (
        os.getenv("EMBEDDING_MODEL") or "text-embedding-3-small"
    ).strip()

    if require_api_key and not api_key:
        print(
            "未检测到 OPENAI_API_KEY。请复制 .env.example 为 .env 并填入密钥。",
            file=sys.stderr,
        )
        sys.exit(1)

    return Settings(
        openai_api_key=api_key,
        openai_base_url=base_url,
        model_name=model_name,
        embedding_model=embedding_model,
        has_api_key=bool(api_key),
    )


def print_settings_summary(settings: Settings) -> None:
    """
    打印脱敏后的配置摘要，便于排障。

    :param settings: 配置快照。
    """
    key_preview = (
        f"{settings.openai_api_key[:6]}...{settings.openai_api_key[-4:]}"
        if settings.has_api_key and len(settings.openai_api_key) > 10
        else ("未设置" if not settings.has_api_key else "***")
    )
    print("=== 运行配置 ===")
    print(f"MODEL_NAME      : {settings.model_name}")
    print(f"EMBEDDING_MODEL : {settings.embedding_model}")
    print(f"OPENAI_BASE_URL : {settings.openai_base_url or '(默认官方)'}")
    print(f"OPENAI_API_KEY  : {key_preview}")


def get_chat_model(*, temperature: float = 0.2):
    """
    使用 init_chat_model 创建聊天模型。

    优先走 langchain 统一入口；若配置了自定义 Base URL，
    则回退到 ChatOpenAI 以保证兼容网关可用。

    :param temperature: 采样温度。
    :return: 可 invoke / stream 的聊天模型实例。
    """
    settings = load_settings(require_api_key=True)

    # 自定义网关：直接用 ChatOpenAI 更稳妥
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

    :return: Embeddings 实例。
    """
    settings = load_settings(require_api_key=True)
    from langchain_openai import OpenAIEmbeddings

    kwargs: dict = {
        "model": settings.embedding_model,
        "api_key": settings.openai_api_key,
    }
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url
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
