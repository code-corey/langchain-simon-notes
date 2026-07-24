"""
共享工具包：统一加载环境变量、创建聊天模型与 Embedding。

各模块小项目通过本包复用配置，避免重复样板代码。
"""

from shared.config import (
    get_chat_model,
    get_embeddings,
    load_settings,
    print_settings_summary,
)

__all__ = [
    "get_chat_model",
    "get_embeddings",
    "load_settings",
    "print_settings_summary",
]
