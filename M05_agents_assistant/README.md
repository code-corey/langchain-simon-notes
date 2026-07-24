# M05 · Agents（create_agent 客服助手）

> 西蒙学习法位置：**第 5 块** —— 把「模型 + 工具 + 循环」组装成可用 Agent。

## 1. 本模块目标

学完后你能：

1. 使用 `create_agent` 创建带工具的 Agent
2. 设计面向业务场景的 system_prompt 与工具集
3. 跑通「电商售后助手」小项目：查订单、查物流、创建工单

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| create_agent | LangChain 高层 Agent 工厂，底层编译为 LangGraph |
| system_prompt | 角色、边界、工具使用策略 |
| agent.invoke | 输入 messages，输出含完整轨迹的 state |
| 业务工具 | 把真实系统 API 伪装成 tool（本项目用内存假数据） |

## 3. 理解层

相对 M04 手写循环，Agent 帮你托管：

- 何时停
- 如何把 ToolMessage 塞回状态
- （可选）中间件、结构化最终输出、checkpointer

你的责任转移到：**工具设计、提示词边界、失败处理**。

## 4. 小项目：电商售后助手

| 文件 | 作用 |
|------|------|
| `store.py` | 内存订单/物流/工单数据 |
| `support_tools.py` | 查询与建单工具 |
| `agent_app.py` | create_agent 组装 |
| `main.py` | CLI 客服台 |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M05_agents_assistant.main
# 试试：
#   帮我查订单 A1001 的状态
#   A1002 物流到哪了？
#   我的包裹破损了，帮我开工单，订单 A1001
```

预设订单：`A1001`（已发货）、`A1002`（运输中）、`A1003`（已签收）。

## 5. 巩固层

### 自检题

1. create_agent 相比手写 loop 隐藏了哪些细节？
2. 若用户问题不含订单号，Agent 应该追问还是瞎猜？如何用 prompt 约束？
3. 为什么售后场景适合「少量高价值工具」而不是上百个模糊工具？

### 刻意练习

- 增加 `cancel_order` 工具，并在 prompt 中限制「已发货不可取消」
- 观察 `result["messages"]` 里工具调用轨迹

### 进入 M06 前置

- [ ] 能独立 create_agent(model, tools, system_prompt)
- [ ] 客服小项目三条主路径跑通

## 6. 衔接

M06 引入 **Middleware**：在不改业务工具的前提下，动态改 prompt / 选模型 / 过滤工具。
