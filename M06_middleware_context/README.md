# M06 · Middleware 与 Context Engineering

> 西蒙学习法位置：**第 6 块** —— 在 Agent 外围「可编程地」注入策略。

## 1. 本模块目标

学完后你能：

1. 理解 Context Engineering：控制模型「看见什么」
2. 使用 `dynamic_prompt` / `wrap_model_call` 中间件
3. 跑通「按用户等级动态改提示 + 按轮次限制工具」的支持台小项目

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| Middleware | 插在 Agent 模型调用前后的钩子 |
| dynamic_prompt | 每次调用前动态生成 system prompt |
| wrap_model_call | 包装模型调用：可改 model / tools / 请求 |
| runtime context | 调用时传入的静态/会话上下文（如用户等级） |
| state | Agent 运行中的可变状态（如 messages） |

## 3. 理解层

不要把所有策略塞进一个巨型 system prompt。更可维护的做法：

```text
固定角色（少） + 中间件动态拼装（按用户/轮次/检索结果）
```

本项目演示两类策略：

1. **VIP / 普通用户** → 不同服务口径（dynamic_prompt）
2. **对话轮次变长** → 收紧可用工具，降低乱跑工具的概率（wrap_model_call）

## 4. 小项目：策略化支持台

| 文件 | 作用 |
|------|------|
| `context_tools.py` | 查知识库条目、查账号权益 |
| `middleware_app.py` | dynamic_prompt + wrap_model_call + create_agent |
| `main.py` | CLI：可切换 --tier vip|normal |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M06_middleware_context.main --tier vip
python -m M06_middleware_context.main --tier normal
```

试试：

- 「我的账号有什么权益？」
- 「退货期限是多久？」
- 连续多轮后再问权益，观察工具是否被收紧

## 5. 巩固层

### 自检题

1. dynamic_prompt 和写死 system_prompt 的分工是什么？
2. 为什么「先注册全部工具，再在中间件里过滤」是推荐模式？
3. context 与 checkpointer state 有何不同？

### 刻意练习

- 增加 `enterprise` 等级，给出不同 SLA 文案
- 在 wrap_model_call 里根据关键词强制只开放知识库工具

### 进入 M07 前置

- [ ] 能读懂并修改至少一种 middleware
- [ ] 理解：RAG 常常通过 middleware / tool 把检索结果注入上下文

## 6. 衔接

M07 把「私有文档」接进来：切分 → Embedding → 向量检索 → Agentic RAG。
