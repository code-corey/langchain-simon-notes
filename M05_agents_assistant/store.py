"""
售后场景的内存数据存储。

用字典模拟订单、物流与工单，避免依赖真实电商后台。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime


@dataclass
class Order:
    """订单记录。"""

    order_id: str
    product: str
    status: str
    user: str
    amount: float


@dataclass
class Shipment:
    """物流记录。"""

    order_id: str
    carrier: str
    tracking_no: str
    last_event: str


@dataclass
class Ticket:
    """售后工单。"""

    ticket_id: str
    order_id: str
    reason: str
    created_at: str
    status: str = "open"


class SupportStore:
    """
    内存版售后数据中心。

    提供订单查询、物流查询与工单创建，供工具函数调用。
    """

    def __init__(self) -> None:
        """初始化演示数据。"""
        self.orders: dict[str, Order] = {
            "A1001": Order("A1001", "机械键盘", "已发货", "张三", 399.0),
            "A1002": Order("A1002", "显示器支架", "运输中", "李四", 159.0),
            "A1003": Order("A1003", "USB-C 扩展坞", "已签收", "王五", 229.0),
        }
        self.shipments: dict[str, Shipment] = {
            "A1001": Shipment("A1001", "顺丰", "SF10001", "已揽收，待转运"),
            "A1002": Shipment("A1002", "京东", "JD20002", "到达华南转运中心"),
            "A1003": Shipment("A1003", "圆通", "YT30003", "本人签收"),
        }
        self.tickets: list[Ticket] = []
        self._ticket_seq = 1

    def get_order(self, order_id: str) -> dict | None:
        """
        按订单号查询订单。

        :param order_id: 订单号。
        :return: 订单字典或 None。
        """
        order = self.orders.get(order_id.upper())
        return asdict(order) if order else None

    def get_shipment(self, order_id: str) -> dict | None:
        """
        按订单号查询物流。

        :param order_id: 订单号。
        :return: 物流字典或 None。
        """
        shipment = self.shipments.get(order_id.upper())
        return asdict(shipment) if shipment else None

    def create_ticket(self, order_id: str, reason: str) -> dict:
        """
        创建售后工单。

        :param order_id: 订单号。
        :param reason: 问题原因。
        :return: 新建工单字典。
        """
        order_id = order_id.upper()
        if order_id not in self.orders:
            raise ValueError(f"订单不存在：{order_id}")
        ticket = Ticket(
            ticket_id=f"T{self._ticket_seq:04d}",
            order_id=order_id,
            reason=reason,
            created_at=datetime.now().isoformat(timespec="seconds"),
        )
        self._ticket_seq += 1
        self.tickets.append(ticket)
        return asdict(ticket)

    def snapshot(self) -> dict:
        """
        导出当前数据快照（调试用）。

        :return: 含订单与工单的字典。
        """
        return {
            "orders": {k: asdict(v) for k, v in self.orders.items()},
            "tickets": [asdict(t) for t in self.tickets],
        }


# 进程内单例，保证多轮工具调用读写同一份数据
STORE = SupportStore()
