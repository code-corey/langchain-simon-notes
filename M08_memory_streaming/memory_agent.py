"""
带短期记忆与流式输出的学习伙伴 Agent。
"""

from __future__ import annotations

from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver


@tool
def save_learning_goal(goal: str) -> str:
    """
    记录用户当前学习目标（演示用工具，结果仍会进入对话轨迹）。

    Args:
        goal: 学习目标简述。
    """
    return f"已记录学习目标：{goal}"


def build_memory_agent(model):
    """
    创建带 InMemorySaver 的 Agent。

    :param model: 聊天模型。
    :return: agent。
    """
    return create_agent(
        model,
        tools=[save_learning_goal],
        system_prompt=(
            "你是长期陪伴的学习伙伴，用中文交流。"
            "利用对话历史记住用户目标与进度；需要明确固化目标时可调用 save_learning_goal。"
            "回答要短、可执行，一次只推进一小步（西蒙：小块掌握）。"
        ),
        checkpointer=InMemorySaver(),
    )


def ask_with_memory(agent, text: str, *, thread_id: str) -> str:
    """
    在指定线程上 invoke，返回最终文本。

    :param agent: 带 checkpointer 的 agent。
    :param text: 用户输入。
    :param thread_id: 会话线程 ID。
    :return: 助手回复。
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content": text}]},
        {"configurable": {"thread_id": thread_id}},
    )
    last = result["messages"][-1]
    content = getattr(last, "content", str(last))
    return content if isinstance(content, str) else str(content)


def stream_with_memory(agent, text: str, *, thread_id: str) -> str:
    """
    在指定线程上流式输出助手文本，并返回拼接结果。

    :param agent: agent。
    :param text: 用户输入。
    :param thread_id: 线程 ID。
    :return: 完整回复文本。
    """
    parts: list[str] = []
    # 不同版本 stream 事件结构可能略有差异，这里做兼容解析
    stream_iter = agent.stream(
        {"messages": [{"role": "user", "content": text}]},
        {"configurable": {"thread_id": thread_id}},
        stream_mode="messages",
    )
    for item in stream_iter:
        token_text = _extract_stream_text(item)
        if token_text:
            print(token_text, end="", flush=True)
            parts.append(token_text)
    print()
    return "".join(parts)


def _extract_stream_text(item) -> str:
    """
    从 stream 事件中尽量提取文本增量。

    :param item: stream 产出的元素。
    :return: 文本增量，没有则空串。
    """
    # stream_mode="messages" 常见为 (message_chunk, metadata)
    if isinstance(item, tuple) and item:
        message = item[0]
    else:
        message = item

    if message is None:
        return ""
    text = getattr(message, "text", None)
    if isinstance(text, str) and text:
        return text
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    return ""
