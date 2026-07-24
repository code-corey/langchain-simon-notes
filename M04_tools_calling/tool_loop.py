"""
手写 tool-calling 循环。

演示：模型提议工具 → 本地执行 → ToolMessage 回灌 → 最终回答。
"""

from __future__ import annotations

from langchain.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

from M04_tools_calling.tools_lib import all_tools


def run_tool_loop(model, user_text: str, *, max_rounds: int = 5) -> str:
    """
    执行最多 max_rounds 轮工具循环，返回最终助手文本。

    :param model: 尚未 bind_tools 的聊天模型。
    :param user_text: 用户问题。
    :param max_rounds: 防止死循环的上限。
    :return: 最终自然语言回答。
    """
    tools = all_tools()
    tools_by_name = {t.name: t for t in tools}
    model_with_tools = model.bind_tools(tools)

    messages = [
        SystemMessage(
            content=(
                "你是桌面助手。需要算数、查时间或搜本地笔记时，必须调用工具。"
                "得到工具结果后再用中文给出简洁最终回答。"
            )
        ),
        HumanMessage(content=user_text),
    ]

    for _ in range(max_rounds):
        ai_msg: AIMessage = model_with_tools.invoke(messages)
        messages.append(ai_msg)

        tool_calls = getattr(ai_msg, "tool_calls", None) or []
        if not tool_calls:
            return _to_text(ai_msg)

        for call in tool_calls:
            name = call["name"]
            args = call.get("args") or {}
            call_id = call["id"]
            tool = tools_by_name.get(name)
            if tool is None:
                result = f"未知工具：{name}"
            else:
                result = tool.invoke(args)
            messages.append(
                ToolMessage(content=str(result), tool_call_id=call_id)
            )

    return "达到工具循环上限，请简化问题后重试。"


def _to_text(message) -> str:
    """
    提取消息文本。

    :param message: AIMessage 或兼容对象。
    :return: 文本。
    """
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return str(content)
