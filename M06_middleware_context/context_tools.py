"""
策略化支持台使用的工具。
"""

from __future__ import annotations

from langchain.tools import tool

KNOWLEDGE = {
    "退货": "自签收起 7 天内可无理由退货，商品需不影响二次销售。",
    "换货": "质量问题 15 天内可换货，需提供开箱视频。",
    "发票": "订单完成后可在 App「我的-发票」申请电子发票。",
}

BENEFITS = {
    "normal": ["标准物流", "7 天无理由"],
    "vip": ["标准物流", "7 天无理由", "专属客服", "运费险"],
}


@tool
def lookup_policy(topic: str) -> str:
    """
    查询售后政策知识。

    Args:
        topic: 主题关键字，如 退货 / 换货 / 发票。
    """
    for key, value in KNOWLEDGE.items():
        if key in topic:
            return value
    return "未找到精确政策，请换用：退货、换货、发票。"


@tool
def lookup_benefits(tier: str) -> str:
    """
    查询账号等级对应权益。

    Args:
        tier: 账号等级，normal 或 vip。
    """
    items = BENEFITS.get(tier.lower())
    if not items:
        return "未知等级。请使用 normal 或 vip。"
    return "、".join(items)


def all_context_tools():
    """
    返回本模块工具列表。

    :return: Tool 列表。
    """
    return [lookup_policy, lookup_benefits]
