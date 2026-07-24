"""
进程内多轮会话：维护 Message 列表并调用模型。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from langchain.messages import AIMessage, HumanMessage, SystemMessage


@dataclass
class ChatSession:
    """
    学习助教会话状态。

    内部保存完整消息列表；每次用户提问都把历史一起发给模型。
    """

    system_prompt: str
    messages: list = field(default_factory=list)
    use_stream: bool = False

    def __post_init__(self) -> None:
        """初始化时写入 SystemMessage。"""
        self.messages = [SystemMessage(content=self.system_prompt)]

    def reset_persona(self, system_prompt: str) -> None:
        """
        切换人设并清空历史（保留新的系统消息）。

        :param system_prompt: 新的系统提示词。
        """
        self.system_prompt = system_prompt
        self.messages = [SystemMessage(content=system_prompt)]

    def ask(self, model, user_text: str) -> str:
        """
        追加用户消息，invoke 模型，并把 AI 回复写回历史。

        :param model: 聊天模型实例。
        :param user_text: 用户输入。
        :return: 助手回复文本。
        """
        self.messages.append(HumanMessage(content=user_text))
        response = model.invoke(self.messages)
        text = _message_to_text(response)
        self.messages.append(AIMessage(content=text))
        return text

    def ask_stream(self, model, user_text: str) -> str:
        """
        流式调用模型，边打印边拼接完整回复，并写入历史。

        :param model: 聊天模型实例。
        :param user_text: 用户输入。
        :return: 拼接后的完整回复。
        """
        self.messages.append(HumanMessage(content=user_text))
        parts: list[str] = []
        for chunk in model.stream(self.messages):
            piece = _message_to_text(chunk)
            if piece:
                print(piece, end="", flush=True)
                parts.append(piece)
        print()
        text = "".join(parts)
        self.messages.append(AIMessage(content=text))
        return text

    def history_preview(self) -> str:
        """
        生成可读的历史预览。

        :return: 多行文本。
        """
        lines: list[str] = []
        for msg in self.messages:
            role = msg.__class__.__name__.replace("Message", "")
            content = _message_to_text(msg)
            if len(content) > 120:
                content = content[:117] + "..."
            lines.append(f"[{role}] {content}")
        return "\n".join(lines)


def _message_to_text(message) -> str:
    """
    从 Message / Chunk 中提取文本。

    :param message: 模型返回对象。
    :return: 文本内容。
    """
    if message is None:
        return ""
    if isinstance(message, str):
        return message
    text = getattr(message, "text", None)
    if isinstance(text, str) and text:
        return text
    content = getattr(message, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict) and block.get("type") == "text":
                parts.append(str(block.get("text", "")))
        return "".join(parts)
    return str(message)
