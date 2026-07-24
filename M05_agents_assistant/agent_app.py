"""
组装售后 create_agent。
"""

from __future__ import annotations

from langchain.agents import create_agent

from M05_agents_assistant.support_tools import support_tools

SYSTEM_PROMPT = """
你是电商售后助手，用中文服务用户。
规则：
1. 查订单、查物流、建工单时必须调用对应工具，不要编造数据。
2. 如果用户没提供订单号，先礼貌追问订单号。
3. 最终回复简洁，包含关键状态；创建工单后要回报工单号。
4. 不要承诺退款到账时间等系统外无法验证的事项。
""".strip()


def build_support_agent(model):
    """
    创建售后 Agent。

    :param model: 聊天模型或模型名字符串。
    :return: 可 invoke 的 agent。
    """
    return create_agent(
        model,
        tools=support_tools(),
        system_prompt=SYSTEM_PROMPT,
    )


def ask_agent(agent, user_text: str) -> str:
    """
    向 Agent 提问并提取最终文本回复。

    :param agent: create_agent 返回对象。
    :param user_text: 用户输入。
    :return: 最终助手文本。
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]}
    )
    messages = result.get("messages") or []
    if not messages:
        return str(result)
    last = messages[-1]
    content = getattr(last, "content", None)
    if isinstance(content, str):
        return content
    return str(last)
