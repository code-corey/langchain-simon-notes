# LangChain 短期记忆笔记

短期记忆通常通过 checkpointer 实现：同一个 thread_id 下，对话状态会被保存。
这样 Agent 可以在多轮中记住用户说过的名字、偏好与未完成任务。
