"""
生产化自检清单（学习用）。

上线前用这些问题逼自己把「演示脚本」升级成「可运维服务」。
"""

from __future__ import annotations

CHECKLIST: list[tuple[str, str]] = [
    ("密钥与配置", "密钥是否只来自环境变量/密钥管理，且未写入仓库？"),
    ("模型超时", "是否设置 timeout / max_retries，避免请求挂死？"),
    ("工具安全", "工具是否校验参数、最小权限、对外部副作用可审计？"),
    ("会话隔离", "thread_id / 用户身份是否正确隔离，避免串话？"),
    ("持久化", "Memory/向量库是否使用可持久后端，而不是进程内存？"),
    ("可观测", "是否接入 LangSmith 或等价 tracing，能回放一次失败调用？"),
    ("流式与取消", "长回答是否支持流式？客户端断开时能否取消？"),
    ("评测", "是否有最小黄金集（10～50 条）做回归？"),
    ("降级", "模型/检索失败时是否有明确降级文案与告警？"),
    ("成本", "是否限制 max_tokens、工具循环次数与并发？"),
]


def render_checklist() -> str:
    """
    渲染可读的生产化清单。

    :return: 多行文本。
    """
    lines = ["=== Agent 生产化检查清单 ==="]
    for i, (title, question) in enumerate(CHECKLIST, start=1):
        lines.append(f"{i:02d}. [{title}] {question}")
    return "\n".join(lines)
