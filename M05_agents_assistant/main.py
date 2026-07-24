"""
M05 小项目：电商售后助手 CLI。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M05_agents_assistant.agent_app import ask_agent, build_support_agent
from shared.config import get_chat_model, load_settings, print_settings_summary


def main() -> int:
    """
    启动售后助手。

    :return: 退出码。
    """
    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0)
    agent = build_support_agent(model)

    print("电商售后助手。示例订单：A1001 / A1002 / A1003。输入 /quit 退出。")
    print("-" * 48)

    while True:
        try:
            user_input = input("用户> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            return 0
        if not user_input:
            continue
        if user_input in {"/quit", "/exit", "/q"}:
            print("再见。")
            return 0
        reply = ask_agent(agent, user_input)
        print(f"助手> {reply}")


if __name__ == "__main__":
    raise SystemExit(main())
