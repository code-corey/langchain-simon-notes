# M08 · Memory、Streaming 与生产化入门

> 西蒙学习法位置：**第 8 块（本路线收束）** —— 让 Agent 可连续对话、可流式反馈、可上线检查。

## 1. 本模块目标

学完后你能：

1. 用 `InMemorySaver` + `thread_id` 实现短期记忆
2. 使用 `agent.stream` 做流式输出
3. 对照生产化清单评估一个 Agent 应用是否「能上线试运行」
4. 跑通「带记忆的流式学习伙伴」小项目

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| Checkpointer | 把 Agent 状态持久化的组件 |
| thread_id | 会话隔离键：同 id 共享记忆，不同 id 互不干扰 |
| Short-term memory | 线程内多轮上下文（本模块重点） |
| stream / stream_mode | 边生成边输出；可订阅 messages/updates 等 |
| LangSmith | 追踪与评测（配置项见 `.env.example`） |

## 3. 理解层

M02 的「消息列表记忆」只活在当前进程对象里；  
M08 的 checkpointer 让**同 thread 的多次 invoke**自动带上历史状态。

```text
agent = create_agent(..., checkpointer=InMemorySaver())
config = {"configurable": {"thread_id": "u-001"}}

invoke#1(config) → 记住「我叫小明」
invoke#2(config) → 能回答「我叫什么」
invoke(其他 thread) → 不记得小明
```

生产化不是「再学一个 API」，而是检查：密钥、超时、工具幂等、可观测、回滚、评测集。

## 4. 小项目：带记忆的流式学习伙伴

| 文件 | 作用 |
|------|------|
| `memory_agent.py` | checkpointer agent + 流式打印 |
| `prod_checklist.py` | 生产化自检项（可打印） |
| `main.py` | CLI：`/thread` 切换会话，默认流式 |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M08_memory_streaming.main
# 命令：
#   /thread <id>     切换会话线程
#   /checklist       打印生产化清单
#   /quit
# 对话试试：
#   记住：我正在学 LangGraph
#   我在学什么？
```

## 5. 巩固层

### 自检题

1. 换一个 thread_id 后为什么「不认识你」？
2. InMemorySaver 重启进程后记忆还在吗？生产该换什么？
3. 流式输出对 UX 与超时控制分别有什么价值？

### 刻意练习

- 开两个 thread，分别设定不同学习目标，交叉提问验证隔离
- 把 `.env` 里 LangSmith 相关项读一遍（即使暂不启用）

### 路线收束

完成本模块后，建议回到 `LEARNING_PATH.md` 做一次「默写知识树」：  
从 Messages → Tools → Agent → Middleware → RAG → Memory，不看文档画出依赖。

## 6. 下一步（可选进阶）

- 用 LangGraph 手写自定义 Graph（分支、人工审批 interrupt）
- 向量库换持久化方案；checkpointer 换 Sqlite/Postgres
- 建立 LangSmith dataset 做回归评测
