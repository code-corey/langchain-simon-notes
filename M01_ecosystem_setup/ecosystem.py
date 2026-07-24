"""
M01 生态地图纯文本说明。

不依赖网络与 API，用于在环境诊断前先建立认知结构。
"""


def render_ecosystem_map() -> str:
    """
    渲染 LangChain 生态认知地图。

    :return: 多行说明文本。
    """
    return """
┌─────────────────────────────────────────────────────────────┐
│                    LangChain 生态认知地图                     │
├─────────────────────────────────────────────────────────────┤
│  你的应用                                                    │
│    └─ create_agent / 自定义 Graph                            │
│         ├─ Models（聊天模型）          ← M02                 │
│         ├─ Messages / Prompts          ← M02 / M03           │
│         ├─ Tools                       ← M04                 │
│         ├─ Middleware / Context        ← M06                 │
│         ├─ Retrieval / RAG             ← M07                 │
│         └─ Checkpointer / Streaming    ← M08                 │
│                                                              │
│  运行时底座：LangGraph（状态、循环、持久化、中断）             │
│  观测评测：LangSmith（trace、dataset、eval）                  │
└─────────────────────────────────────────────────────────────┘

决策口诀：
  · 单次问答 / 结构化抽取 → 直接用 Chat Model（M02-M03）
  · 需要调用外部能力、多步推理 → Agent + Tools（M04-M05）
  · 需要私有知识 → RAG（M07）
  · 需要跨轮记住对话 → Memory / Checkpointer（M08）
""".strip()
