# M04 · Tools 与 Tool Calling

> 西蒙学习法位置：**第 4 块** —— 让模型「会做事」，而不只是「会说话」。

## 1. 本模块目标

学完后你能：

1. 用 `@tool` 定义可被模型调用的函数
2. 理解 `bind_tools` → `tool_calls` → 执行 → 回填的人工循环
3. 跑通「桌面工具箱」小项目：计算器、时间、笔记检索（本地）

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| Tool | 带名称、描述、参数 schema 的可执行能力 |
| bind_tools | 把工具 schema 挂到模型上，使其能发出 tool_calls |
| tool_calls | 模型声明「我要调哪个工具、参数是什么」 |
| 工具循环 | 模型提议 → 程序执行 → 结果作为 ToolMessage 回灌 → 再生成最终回答 |

## 3. 理解层

工具不是魔法：模型只负责**提议**；**执行权在你的代码**。

```text
用户问题
  → model.bind_tools([...]).invoke(messages)
  → 若有 tool_calls：执行本地函数，追加 ToolMessage
  → 再 invoke，直到模型给出最终自然语言答案
```

M05 的 `create_agent` 会自动托管这个循环；本模块刻意手写一遍，打牢直觉。

## 4. 小项目：桌面工具箱

| 文件 | 作用 |
|------|------|
| `tools_lib.py` | 计算器、当前时间、本地笔记搜索 |
| `tool_loop.py` | 手写 tool-calling 循环 |
| `main.py` | CLI 问答 |
| `notes/` | 供检索的本地笔记 |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M04_tools_calling.main
# 试试：
#   现在几点？
#   计算 (3.5+2)*8
#   笔记里有没有提到 checkpoint？
```

## 5. 巩固层

### 自检题

1. 为什么工具的 docstring / 参数描述质量直接影响成功率？
2. 如果模型乱造参数，你的函数侧应如何防御？
3. 手写循环与 create_agent 各适合什么场景？

### 刻意练习

- 新增一个 `list_note_titles` 工具并验证模型会选它
- 故意把某个工具描述写得很模糊，观察误调用率变化

### 进入 M05 前置

- [ ] 能独立写 `@tool` + 手写一轮 tool loop
- [ ] 理解：Agent = 模型 + 工具 + 循环策略（+ 中间件/记忆）

## 6. 衔接

M05 用 `create_agent` 把工具循环产品化，做成「客服助手」完整小项目。
