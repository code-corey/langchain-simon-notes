"""
M02 小项目：多角色学习助教 CLI。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M02_models_messages.chat_session import ChatSession
from M02_models_messages.personas import get_persona_prompt, list_persona_names
from shared.config import get_chat_model, print_settings_summary, load_settings


def main() -> int:
    """
    启动交互式助教。

    :return: 退出码。
    """
    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0.4)

    persona = "tutor"
    session = ChatSession(system_prompt=get_persona_prompt(persona))

    print("多角色学习助教已启动。")
    print(f"当前人设：{persona}（可选：{', '.join(list_persona_names())}）")
    print("命令：/persona <名>  /stream on|off  /history  /quit")
    print("-" * 48)

    while True:
        try:
            user_input = input("你> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n再见。")
            return 0

        if not user_input:
            continue

        if user_input.startswith("/"):
            handled = _handle_command(user_input, session)
            if handled == "quit":
                print("再见。")
                return 0
            continue

        print("助教> ", end="", flush=True)
        if session.use_stream:
            session.ask_stream(model, user_input)
        else:
            print(session.ask(model, user_input))


def _handle_command(command: str, session: ChatSession) -> str | None:
    """
    处理斜杠命令。

    :param command: 用户输入的命令。
    :param session: 当前会话。
    :return: 若退出则返回 "quit"，否则返回 None。
    """
    parts = command.split()
    name = parts[0].lower()

    if name in {"/quit", "/exit", "/q"}:
        return "quit"

    if name == "/history":
        print(session.history_preview())
        return None

    if name == "/stream":
        if len(parts) < 2 or parts[1] not in {"on", "off"}:
            print("用法：/stream on|off")
            return None
        session.use_stream = parts[1] == "on"
        print(f"流式输出：{'开' if session.use_stream else '关'}")
        return None

    if name == "/persona":
        if len(parts) < 2:
            print(f"用法：/persona {'|'.join(list_persona_names())}")
            return None
        try:
            prompt = get_persona_prompt(parts[1])
        except KeyError as exc:
            print(exc)
            return None
        session.reset_persona(prompt)
        print(f"已切换人设为：{parts[1]}（历史已清空）")
        return None

    print("未知命令。可用：/persona /stream /history /quit")
    return None


if __name__ == "__main__":
    raise SystemExit(main())
