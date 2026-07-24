"""
M04 小项目：桌面工具箱 CLI。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M04_tools_calling.tool_loop import run_tool_loop
from shared.config import get_chat_model, load_settings, print_settings_summary


def main() -> int:
    """
    启动工具箱交互问答。

    :return: 退出码。
    """
    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0)

    print("桌面工具箱（手写 tool loop）。输入 /quit 退出。")
    print("可用能力：计算器 / 当前时间 / 本地笔记搜索")
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
        answer = run_tool_loop(model, user_input)
        print(f"助手> {answer}")


if __name__ == "__main__":
    raise SystemExit(main())
