# M02 · Chat Models 与 Messages

> 西蒙学习法位置：**第 2 块** —— 掌握 LLM 应用的最小交互单元。

## 1. 本模块目标

学完后你能：

1. 用 `init_chat_model` / `ChatOpenAI` 创建模型并 `invoke` / `stream`
2. 正确组装 `SystemMessage` / `HumanMessage` / `AIMessage` 多轮对话
3. 跑通「多角色学习助教」小项目：系统人设 + 多轮记忆（进程内）+ 流式输出

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| Chat Model | 面向「消息列表进、消息出」的对话模型抽象 |
| Message | 带角色的内容单元：system / human / ai / tool |
| invoke | 一次性拿完整回复 |
| stream | 按 token/chunk 流式返回，适合交互 UI |
| 多轮对话 | 把历史 AI/Human 消息继续放进列表再调用 |

## 3. 理解层

把模型想成「只看见你塞进去的消息列表」的函数：

```text
messages = [System, Human, AI, Human, ...]  →  model.invoke(messages)  →  AIMessage
```

常见错误：只发最新一句用户话，却期望模型「记得」之前内容——**没有外部记忆时，历史必须你自己带上**（M08 才会讲 checkpointer）。

## 4. 小项目：多角色学习助教

| 文件 | 作用 |
|------|------|
| `main.py` | 交互式 CLI：选人设、多轮聊天、`/stream` 切换流式 |
| `personas.py` | 预设系统人设 |
| `chat_session.py` | 会话状态（消息列表）管理 |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M02_models_messages.main
# 命令：
#   /persona tutor|coach|socratic   切换人设
#   /stream on|off                  开关流式
#   /history                        查看消息
#   /quit                           退出
```

## 5. 巩固层

### 自检题

1. `SystemMessage` 和 `HumanMessage` 分别影响什么？
2. 流式输出时，最终完整文本如何拼出来？
3. 为什么「刷新进程后对话全丢」？这和 M08 的 memory 有何关系？

### 刻意练习

- 新增一个人设（例如「代码审查员」），改 `personas.py` 后验证
- 对比同一问题在 `invoke` 与 `stream` 下的体感差异

### 进入 M03 前置

- [ ] 能手写一段含三种 Message 的调用
- [ ] 助教小项目能多轮正常对话
- [ ] 理解：无持久化时历史靠消息列表

## 6. 衔接

M03 会在「自由文本回复」之上，加上 **Prompt 模板 + 结构化输出（Pydantic）**。
