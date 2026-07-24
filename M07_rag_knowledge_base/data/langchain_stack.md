# LangChain 学习栈约定

本团队内部约定：

- 聊天模型统一通过 `init_chat_model` 或兼容网关的 `ChatOpenAI` 创建。
- 复杂多步任务使用 `create_agent`，需要精细控制时下沉 LangGraph。
- 私有知识问答优先 RAG：`RecursiveCharacterTextSplitter` + Embeddings + `InMemoryVectorStore`（原型）/ 生产换持久向量库。
- 跨轮对话使用 checkpointer（如 `InMemorySaver`），并用 `thread_id` 区分会话。
- 观测优先接入 LangSmith，关键链路必须可追踪。
