"""
M01 小项目：环境诊断台。

检查 Python 版本、关键依赖、.env 配置，并可选择性地
对聊天模型发起一次 ping，验证密钥与网络是否可用。
"""

from __future__ import annotations

import argparse
import importlib.util
import sys
from pathlib import Path

# 保证从任意 cwd 运行都能找到仓库根
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M01_ecosystem_setup.ecosystem import render_ecosystem_map
from shared.config import load_settings, print_settings_summary


REQUIRED_PACKAGES = [
    "langchain",
    "langchain_core",
    "langchain_openai",
    "langgraph",
    "dotenv",
    "pydantic",
]


def check_python() -> tuple[bool, str]:
    """
    检查 Python 版本是否满足最低要求。

    :return: (是否通过, 说明文字)。
    """
    major, minor = sys.version_info[:2]
    ok = (major, minor) >= (3, 10)
    return ok, f"Python {major}.{minor}.{sys.version_info[2]}（需要 >= 3.10）"


def check_packages() -> list[tuple[str, bool]]:
    """
    逐个检查关键第三方包是否可导入。

    :return: (包名, 是否存在) 列表。
    """
    results: list[tuple[str, bool]] = []
    for name in REQUIRED_PACKAGES:
        # dotenv 的导入名是 dotenv，包名是 python-dotenv
        module_name = "dotenv" if name == "dotenv" else name
        found = importlib.util.find_spec(module_name) is not None
        results.append((name, found))
    return results


def check_env_file() -> tuple[bool, str]:
    """
    检查仓库根目录是否存在 .env。

    :return: (是否存在, 说明文字)。
    """
    env_path = REPO_ROOT / ".env"
    if env_path.exists():
        return True, f"找到 {env_path}"
    return False, f"未找到 {env_path}（可复制 .env.example）"


def ping_model() -> str:
    """
    发起一次最小模型调用，验证聊天服务连通性。

    :return: 模型回复文本。
    """
    from shared.config import get_chat_model

    model = get_chat_model(temperature=0)
    response = model.invoke("用一句话介绍你自己。请用中文回答。")
    text = getattr(response, "content", None) or getattr(response, "text", "") or str(response)
    return str(text)


def ping_embeddings() -> str:
    """
    发起一次最小 embedding 调用，验证向量服务连通性。

    :return: 成功说明（含向量维度）。
    """
    from shared.config import get_embeddings

    embeddings = get_embeddings()
    vectors = embeddings.embed_documents(["连通性探测"])
    dim = len(vectors[0]) if vectors and vectors[0] else 0
    return f"embedding 成功，维度={dim}"


def main(argv: list[str] | None = None) -> int:
    """
    CLI 入口：打印地图、跑诊断，可选 ping 聊天与 embedding。

    :param argv: 命令行参数列表。
    :return: 进程退出码，0 表示全部必检项通过。
    """
    parser = argparse.ArgumentParser(description="M01 环境诊断台")
    parser.add_argument(
        "--ping",
        action="store_true",
        help="额外探测聊天模型与 Embedding 服务连通性",
    )
    args = parser.parse_args(argv)

    print(render_ecosystem_map())
    print()
    print("=== 环境诊断 ===")

    py_ok, py_msg = check_python()
    print(f"[{'OK' if py_ok else 'FAIL'}] {py_msg}")

    pkg_results = check_packages()
    pkg_ok = True
    for name, found in pkg_results:
        print(f"[{'OK' if found else 'FAIL'}] 依赖 {name}")
        pkg_ok = pkg_ok and found

    env_ok, env_msg = check_env_file()
    print(f"[{'OK' if env_ok else 'WARN'}] {env_msg}")

    settings = load_settings(require_api_key=False)
    print_settings_summary(settings)
    key_ok = settings.has_api_key
    print(f"[{'OK' if key_ok else 'WARN'}] 运行配置 {'已就绪' if key_ok else '未就绪'}")

    ping_ok = True
    args.ping = True
    if args.ping:
        print()
        print("=== 服务 Ping ===")
        if not key_ok:
            print("[FAIL] 配置未就绪，无法 ping")
            ping_ok = False
        else:

            try:
                reply = ping_model()
                print("[OK] 聊天模型回复：")
                print(reply)
            except Exception as exc:  # noqa: BLE001 - 诊断场景需要展示任意错误
                print(f"[FAIL] 聊天 ping 失败：{exc}")
                ping_ok = False

            try:
                emb_msg = ping_embeddings()
                print(f"[OK] {emb_msg}")
            except Exception as exc:  # noqa: BLE001
                print(f"[FAIL] embedding ping 失败：{exc}")
                ping_ok = False

    print()
    # .env 与 key 在仅做地图学习时可缺，但标为 WARN；依赖与 Python 必须过
    all_required_ok = py_ok and pkg_ok and (ping_ok if args.ping else True)
    if all_required_ok:
        print("诊断结论：必检项通过，可以进入 M02。")
        return 0

    print("诊断结论：存在失败项，请先按 README 修复。")
    if not pkg_ok:
        print("提示：在仓库根目录执行  pip install -r requirements.txt")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
