"""
售后助手工具集。
"""

from __future__ import annotations

import json

from langchain.tools import tool

from M05_agents_assistant.store import STORE


@tool
def lookup_order(order_id: str) -> str:
    """
    根据订单号查询订单状态与商品信息。

    Args:
        order_id: 订单号，例如 A1001。
    """
    data = STORE.get_order(order_id)
    if not data:
        return f"未找到订单 {order_id}。可用示例：A1001 / A1002 / A1003。"
    return json.dumps(data, ensure_ascii=False)


@tool
def lookup_shipment(order_id: str) -> str:
    """
    根据订单号查询物流轨迹摘要。

    Args:
        order_id: 订单号，例如 A1002。
    """
    data = STORE.get_shipment(order_id)
    if not data:
        return f"未找到订单 {order_id} 的物流信息。"
    return json.dumps(data, ensure_ascii=False)


@tool
def create_support_ticket(order_id: str, reason: str) -> str:
    """
    为指定订单创建售后工单。

    Args:
        order_id: 订单号。
        reason: 用户问题原因，例如「外包装破损」。
    """
    try:
        ticket = STORE.create_ticket(order_id, reason)
    except ValueError as exc:
        return str(exc)
    return json.dumps(ticket, ensure_ascii=False)


def support_tools():
    """
    返回售后工具列表。

    :return: Tool 列表。
    """
    return [lookup_order, lookup_shipment, create_support_ticket]
