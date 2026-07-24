"""
M08 小项目：带记忆的流式学习伙伴。
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M08_memory_streaming.memory_agent import (
    ask_with_memory,
    build_memory_agent,
    stream_with_memory,
)
from M08_memory_streaming.prod_checklist import render_checklist
from shared.config import get_chat_model, load_settings, print_settings_summary


def main() -> int:
    """
    启动带记忆的流式学习伙伴。

    :return: 退出码。
    """
    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0.3)
    agent = build_memory_agent(model)

    thread_id = "default"
    use_stream = True

    print("带记忆的流式学习伙伴已启动。")
    print(f"当前 thread_id={thread_id}，stream={'on' if use_stream else 'off'}")
    print("命令：/thread <id>  /stream on|off  /checklist  /quit")
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
            flag = _handle_command(user_input)
            if flag == "quit":
                print("再见。")
                return 0
            if isinstance(flag, dict):
                if "thread_id" in flag:
                    thread_id = flag["thread_id"]
                    print(f"已切换 thread_id={thread_id}")
                if "use_stream" in flag:
                    use_stream = flag["use_stream"]
                    print(f"stream={'on' if use_stream else 'off'}")
            continue

        print("伙伴> ", end="", flush=True)
        if use_stream:
            try:
                stream_with_memory(agent, user_input, thread_id=thread_id)
            except Exception as exc:  # noqa: BLE001
                print(f"\n流式失败，回退 invoke：{exc}")
                print(ask_with_memory(agent, user_input, thread_id=thread_id))
        else:
            print(ask_with_memory(agent, user_input, thread_id=thread_id))


def _handle_command(command: str):
    """
    处理斜杠命令。

    :param command: 命令文本。
    :return: "quit" | 状态更新 dict | None。
    """
    parts = command.split()
    name = parts[0].lower()
    if name in {"/quit", "/exit", "/q"}:
        return "quit"
    if name == "/checklist":
        print(render_checklist())
        return None
    if name == "/thread":
        if len(parts) < 2:
            print("用法：/thread <id>")
            return None
        return {"thread_id": parts[1]}
    if name == "/stream":
        if len(parts) < 2 or parts[1] not in {"on", "off"}:
            print("用法：/stream on|off")
            return None
        return {"use_stream": parts[1] == "on"}
    print("未知命令。")
    return None


if __name__ == "__main__":
    raise SystemExit(main())
