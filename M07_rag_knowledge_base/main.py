"""
M07 小项目：团队 Wiki 问答 CLI。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M07_rag_knowledge_base.indexer import build_vector_store
from M07_rag_knowledge_base.rag_agent import ask_rag, build_rag_agent
from shared.config import (
    get_chat_model,
    get_embeddings,
    load_settings,
    print_settings_summary,
)


def main() -> int:
    """
    构建索引并启动 Wiki 问答。

    :return: 退出码。
    """
    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)

    print("正在构建内存向量索引……")
    embeddings = get_embeddings()
    store = build_vector_store(embeddings)
    print("索引完成。")

    model = get_chat_model(temperature=0)
    agent = build_rag_agent(model, store)

    print("团队 Wiki 问答已就绪。输入 /quit 退出。")
    print("-" * 48)

    while True:
        try:
            user_input = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            return 0
        if not user_input:
            continue
        if user_input in {"/quit", "/exit", "/q"}:
            print("再见。")
            return 0
        answer = ask_rag(agent, user_input)
        print(f"助手> {answer}")


if __name__ == "__main__":
    raise SystemExit(main())
