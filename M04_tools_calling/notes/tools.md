# 工具调用要点

Tool 的描述要写清楚「何时该用」。参数用类型和 Field/docstring 约束。
模型只负责提出 tool_calls，真正执行在本地代码中完成。
