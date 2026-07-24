"""
带 Middleware 的 Agent 组装。
"""

from __future__ import annotations

from typing import Callable, TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest,
    ModelResponse,
    dynamic_prompt,
    wrap_model_call,
)

from M06_middleware_context.context_tools import all_context_tools, lookup_policy


class UserContext(TypedDict):
    """调用时传入的用户上下文。"""

    user_name: str
    tier: str  # normal | vip


def build_agent(model):
    """
    创建带动态提示与工具过滤的 Agent。

    :param model: 聊天模型。
    :return: agent 实例。
    """
    tools = all_context_tools()

    @dynamic_prompt
    def tier_prompt(request: ModelRequest) -> str:
        """
        按用户等级生成系统提示。

        :param request: 模型请求上下文。
        :return: system prompt 文本。
        """
        ctx = request.runtime.context or {}
        name = ctx.get("user_name", "用户")
        tier = ctx.get("tier", "normal")
        if tier == "vip":
            tone = "你服务的是 VIP 客户，语气更主动，优先给可执行方案。"
        else:
            tone = "你服务的是普通客户，语气礼貌简洁，先给标准政策。"
        return (
            f"你是售后策略助手，用中文回答。客户称呼：{name}。{tone}"
            "需要政策或权益时必须调用工具，不要编造。"
        )

    @wrap_model_call
    def limit_tools_when_long(
        request: ModelRequest,
        handler: Callable[[ModelRequest], ModelResponse],
    ) -> ModelResponse:
        """
        对话变长后收紧工具，仅保留政策查询，降低干扰。

        :param request: 原始模型请求。
        :param handler: 下游处理器。
        :return: 模型响应。
        """
        message_count = len(request.messages)
        if message_count >= 8:
            request = request.override(tools=[lookup_policy])
        else:
            request = request.override(tools=tools)
        return handler(request)

    return create_agent(
        model,
        tools=tools,
        middleware=[tier_prompt, limit_tools_when_long],
        context_schema=UserContext,
    )


def ask(agent, user_text: str, *, user_name: str, tier: str) -> str:
    """
    带着 runtime context 调用 Agent。

    :param agent: Agent。
    :param user_text: 用户输入。
    :param user_name: 用户名。
    :param tier: 等级。
    :return: 最终回复文本。
    """
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_text}]},
        context=UserContext(user_name=user_name, tier=tier),
    )
    last = result["messages"][-1]
    content = getattr(last, "content", str(last))
    return content if isinstance(content, str) else str(content)
