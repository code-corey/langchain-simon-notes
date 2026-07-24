# M01 · 认知地图与环境诊断

> 西蒙学习法位置：**第 1 块（Chunk）** —— 先建「知识地图」，再装「可验证环境」。

## 1. 本模块目标

学完后你能：

1. 用自己的话说清 **LangChain / LangGraph / LangSmith** 各自解决什么问题
2. 画出当前官方推荐的应用架构（Agent-first）
3. 跑通本仓库的环境诊断小项目，确认依赖与密钥就绪

## 2. 知识原子（建议默写）

| 原子 | 一句话 |
|------|--------|
| LangChain | 面向「用 LLM 做事」的高阶抽象与集成层（模型、工具、Agent、中间件等） |
| LangGraph | 更底层的可控运行时：状态图、循环、持久化、人机协同 |
| LangSmith | 观测与评测：追踪调用、调试 Agent、做评测集 |
| Agent-first | 复杂于「单次 LLM 调用」的应用，优先用 Agent / Graph，而不是堆旧式 Chain |
| create_agent | LangChain 高层入口，底层会编译成 LangGraph |

## 3. 理解层：为什么要先学地图？

西蒙强调：**复杂技能必须切成可掌握的小块，并先理解结构再记细节**。

如果你一上来就背 `invoke` / `tool` API，很容易把三层产品混成一团。正确顺序是：

```text
问题 → 是否需要多步决策？
  ├─ 否 → 单次模型调用（M02）即可
  └─ 是 → Agent / Graph（M05+）
           └─ 需要检索外部知识？→ RAG（M07）
           └─ 需要跨轮记忆？→ checkpointer（M08）
```

历史脉络（来自官方 philosophy）：LangChain 早期以 Chain/RAG 闻名；约 2024 起 LangGraph 成为复杂应用首选；今天的 `create_agent` 是建立在 Graph 之上的高阶封装。

## 4. 小项目：环境诊断台

目录：`M01_ecosystem_setup/`

| 文件 | 作用 |
|------|------|
| `main.py` | CLI 入口：检查 Python、依赖、.env、可选模型连通性 |
| `ecosystem.py` | 打印「生态地图」文本说明（不依赖网络） |
| `README.md` | 本解释文档 |

### 运行

```bash
# 在仓库根目录
python -m M01_ecosystem_setup.main
python -m M01_ecosystem_setup.main --ping   # 额外发起一次真实模型调用
```

## 5. 巩固层

### 自检题

1. LangChain 和 LangGraph 谁更底层？复杂循环状态该优先看谁？
2. 为什么说「大多数旧 Chain/Agent 应迁移到 LangGraph / create_agent」？
3. 本仓库为什么用 `.env` + `shared/config.py` 统一模型创建？

### 刻意练习

- 不看文档，手绘一张「应用架构图」：用户 → Agent → Tools / RAG / Memory → LLM
- 故意删掉 `.env` 里的 Key，观察诊断输出，再恢复

### 进入 M02 的前置清单

- [ ] 能口述三件套职责
- [ ] `python -m M01_ecosystem_setup.main` 全部检查通过
- [ ] （推荐）`--ping` 成功拿到模型回复

## 6. 与下一模块的衔接

M02 开始真正调用 **Chat Model + Messages**。地图已就绪，可以进入「最小交互单元」。
