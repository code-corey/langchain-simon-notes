"""
M06 小项目：策略化支持台 CLI。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M06_middleware_context.middleware_app import ask, build_agent
from shared.config import get_chat_model, load_settings, print_settings_summary


def main(argv: list[str] | None = None) -> int:
    """
    启动策略化支持台。

    :param argv: 命令行参数。
    :return: 退出码。
    """
    parser = argparse.ArgumentParser(description="M06 策略化支持台")
    parser.add_argument(
        "--tier",
        choices=["normal", "vip"],
        default="normal",
        help="用户等级",
    )
    parser.add_argument("--name", default="同学", help="用户称呼")
    args = parser.parse_args(argv)

    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0)
    agent = build_agent(model)

    print(f"策略化支持台 | 用户={args.name} | 等级={args.tier}")
    print("输入 /quit 退出。")
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
        reply = ask(
            agent,
            user_input,
            user_name=args.name,
            tier=args.tier,
        )
        print(f"助手> {reply}")


if __name__ == "__main__":
    raise SystemExit(main())
