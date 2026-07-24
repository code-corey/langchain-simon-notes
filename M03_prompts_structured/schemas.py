"""
情报卡数据结构定义。

字段描述会进入模型可见的 schema，描述写清楚能显著提高抽取质量。
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class NewsBrief(BaseModel):
    """技术文章情报卡。"""

    title: str = Field(description="简洁标题，不超过 30 字")
    one_liner: str = Field(description="一句话摘要")
    key_points: list[str] = Field(
        description="3 到 5 个要点，每条一句话",
        min_length=1,
        max_length=5,
    )
    audience: Literal["新手", "进阶", "专家"] = Field(
        description="最适合的读者层级"
    )
    action_items: list[str] = Field(
        description="读者读完后可立即执行的 1 到 3 个行动项",
        min_length=1,
        max_length=3,
    )
    confidence: float = Field(
        description="你对抽取质量的自信度，0 到 1",
        ge=0,
        le=1,
    )
