# 学习路径（西蒙节奏版）

## 总原则

1. **一次只攻一个模块**
2. 模块内顺序：默写原子 → 读理解层 → 跑小项目 → 做自检与练习
3. 前置清单全部勾选后，才进入下一模块
4. 每周用 30 分钟「遮住文档默写知识树」

## 建议日程（可按周压缩/拉长）

| 阶段 | 模块 | 验收标准 |
|------|------|----------|
| Day 1 | M01 | 诊断通过，能口述三件套 |
| Day 2 | M02 | 多轮 + 流式对话正常 |
| Day 3 | M03 | 输出合法情报卡 JSON |
| Day 4 | M04 | 手写 tool loop 三条路径成功 |
| Day 5 | M05 | 售后助手查单/物流/工单成功 |
| Day 6 | M06 | VIP/普通口径差异可感知 |
| Day 7 | M07 | Wiki 问答能引用 source |
| Day 8 | M08 | 同 thread 有记忆，异 thread 隔离；能讲生产清单 |

## 知识树（默写版提纲）

```text
LLM 应用
├── 单次调用
│   ├── Messages
│   ├── Prompt
│   └── Structured Output
└── 多步应用
    ├── Tools + Tool Loop
    ├── create_agent
    ├── Middleware / Context
    ├── RAG（检索当工具或注入上下文）
    └── Memory（checkpointer + thread_id）
         └── 生产化：观测 / 超时 / 评测 / 降级
```

## 主动回忆题库（整条路线）

1. 为什么复杂应用优先 Agent/Graph 而不是堆旧 Chain？
2. Message 列表在无 checkpointer 时扮演什么角色？
3. Tool 调用中「模型」与「宿主程序」各负责什么？
4. Middleware 解决了 prompt 膨胀的什么问题？
5. RAG 的五步是什么？哪一步最影响效果？
6. `thread_id` 丢了意味着什么？

写不出答案 → 回到对应模块 README，不要跳。
