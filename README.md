# LangChain 西蒙学习法笔记

基于 [西蒙学习法](https://zh.wikipedia.org/wiki/%E8%A5%BF%E8%92%99%C2%B7%E5%9F%83%E5%B0%94%E4%BD%AF%E7%89%B9%C2%B7%E8%A5%BF%E8%92%99) 的核心原则——**知识切块、理解结构、主动回忆、刻意练习、层层递进**——整理的 LangChain（Python）学习仓库。

技术内容对齐官方当前主线（Agent-first、`init_chat_model`、`create_agent`、Middleware、RAG、Checkpointer），文档与示例编写时参考了 Context7 拉取的最新 LangChain 文档。

仓库地址（推送后）：`https://github.com/code-corey/langchain-simon-notes`

## 学习地图（8 个完整小项目）

```text
M01 认知地图与环境诊断
 └─ M02 Models & Messages（多角色学习助教）
     └─ M03 Prompts & 结构化输出（情报卡生成器）
         └─ M04 Tools 手写循环（桌面工具箱）
             └─ M05 create_agent（电商售后助手）
                 └─ M06 Middleware（策略化支持台）
                     └─ M07 RAG（团队 Wiki 问答）
                         └─ M08 Memory + Streaming（带记忆的学习伙伴）
```

| 模块 | 小项目 | 解释文档 |
|------|--------|----------|
| M01 | 环境诊断台 | [M01 README](M01_ecosystem_setup/README.md) |
| M02 | 多角色学习助教 | [M02 README](M02_models_messages/README.md) |
| M03 | 技术文章情报卡 | [M03 README](M03_prompts_structured/README.md) |
| M04 | 桌面工具箱 | [M04 README](M04_tools_calling/README.md) |
| M05 | 电商售后助手 | [M05 README](M05_agents_assistant/README.md) |
| M06 | 策略化支持台 | [M06 README](M06_middleware_context/README.md) |
| M07 | 团队 Wiki 问答 | [M07 README](M07_rag_knowledge_base/README.md) |
| M08 | 带记忆的流式学习伙伴 | [M08 README](M08_memory_streaming/README.md) |

更细的节奏与默写清单见 [LEARNING_PATH.md](LEARNING_PATH.md)。

## 快速开始

```bash
cd langchain-simon-notes
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
copy .env.example .env
# 编辑 .env，填入 OPENAI_API_KEY（可选 OPENAI_BASE_URL）
```

按顺序运行：

```bash
python -m M01_ecosystem_setup.main
python -m M01_ecosystem_setup.main --ping
python -m M02_models_messages.main
python -m M03_prompts_structured.main --file M03_prompts_structured/sample_article.txt
python -m M04_tools_calling.main
python -m M05_agents_assistant.main
python -m M06_middleware_context.main --tier vip
python -m M07_rag_knowledge_base.main
python -m M08_memory_streaming.main
```

> 所有模块请在**仓库根目录**执行，以便正确加载 `shared` 与 `.env`。

## 西蒙学习法怎么用本仓库

每个模块 README 都固定四层：

1. **知识原子**：先默写，不求多
2. **理解层**：弄清「为什么」，接到上一块
3. **操作层**：跑完整小项目，不是碎片 snippet
4. **巩固层**：自检题 + 刻意练习 + 进入下一块的前置清单

建议节奏：一块未过自检，不进入下一块。

## 配置说明

| 变量 | 含义 |
|------|------|
| `OPENAI_API_KEY` | API 密钥 |
| `OPENAI_BASE_URL` | 可选，OpenAI Compatible 网关 |
| `MODEL_NAME` | 如 `openai:gpt-4o-mini` |
| `EMBEDDING_MODEL` | RAG 用 embedding 模型 |

公共工厂：`shared/config.py`。

## 目录结构

```text
langchain-simon-notes/
├── README.md
├── LEARNING_PATH.md
├── requirements.txt
├── .env.example
├── shared/                 # 公共配置
├── M01_ecosystem_setup/
├── M02_models_messages/
├── M03_prompts_structured/
├── M04_tools_calling/
├── M05_agents_assistant/
├── M06_middleware_context/
├── M07_rag_knowledge_base/
└── M08_memory_streaming/
```

## License

MIT
