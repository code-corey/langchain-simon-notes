# M03 · Prompts 与结构化输出

> 西蒙学习法位置：**第 3 块** —— 从「自由文本」升级到「可被程序消费的结构」。

## 1. 本模块目标

学完后你能：

1. 用 ChatPromptTemplate（或等价消息拼装）组织可复用提示
2. 用 Pydantic + `with_structured_output` 拿到类型安全结果
3. 跑通「技术文章情报卡」小项目：输入一段文本 → 输出结构化情报卡 JSON

## 2. 知识原子

| 原子 | 一句话 |
|------|--------|
| Prompt Template | 把可变槽位（主题、语气、原文）从固定指令中分离 |
| Structured Output | 约束模型按 schema 返回（字段、类型、校验） |
| Pydantic BaseModel | 既是业务模型，也是给模型看的 schema 描述 |
| with_structured_output | 模型侧封装：自动解析并校验为指定类型 |

## 3. 理解层

自由文本适合给人看；**流水线 / Agent 下游**更需要结构化：

```text
原文 → Prompt（角色+任务+约束）→ 结构化模型 → NewsBrief 对象 → 存库 / 展示 / 再处理
```

西蒙视角：先掌握「输出必须可验证」这一块，后面做 Tool / Agent 时才不会把半成品字符串当接口。

## 4. 小项目：技术文章情报卡生成器

| 文件 | 作用 |
|------|------|
| `schemas.py` | Pydantic 情报卡模型 |
| `extractor.py` | Prompt + structured output 管线 |
| `main.py` | CLI：读文件或标准输入，打印 JSON |
| `sample_article.txt` | 示例原文 |
| `README.md` | 本解释文档 |

### 运行

```bash
python -m M03_prompts_structured.main --file M03_prompts_structured/sample_article.txt
python -m M03_prompts_structured.main --text "LangGraph 让 Agent 状态可持久化……"
```

## 5. 巩固层

### 自检题

1. 为什么 Field(description=...) 对结构化抽取很重要？
2. 结构化失败时（校验错误）你该如何排查：Prompt、schema 还是模型能力？
3. 结构化输出和「让模型自己打印 JSON」有何本质区别？

### 刻意练习

- 给 `NewsBrief` 增加字段 `risk_level: Literal["low","mid","high"]` 并验证
- 用同一 schema 抽两篇不同文章，对比字段完整度

### 进入 M04 前置

- [ ] 能独立写一个 Pydantic schema + with_structured_output
- [ ] 小项目能输出合法 JSON
- [ ] 理解：结构化是给程序用的契约

## 6. 衔接

M04 把「模型可调用的外部能力」做成 **Tool**；Tool 的参数定义同样依赖清晰 schema。
