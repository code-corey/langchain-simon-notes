"""
桌面工具箱：供模型调用的本地能力。
"""

from __future__ import annotations

import ast
import operator
from datetime import datetime
from pathlib import Path

from langchain.tools import tool

NOTES_DIR = Path(__file__).resolve().parent / "notes"

# 安全计算器：仅允许字面量与四则运算
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.Pow: operator.pow,
}


def _eval_node(node: ast.AST) -> float:
    """
    递归计算 AST 节点（仅允许安全子集）。

    :param node: AST 节点。
    :return: 数值结果。
    """
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _eval_node(node.left),
            _eval_node(node.right),
        )
    raise ValueError("仅支持数字与 + - * / ** 运算")


@tool
def calculate(expression: str) -> str:
    """
    计算数学表达式，支持加减乘除与幂运算。

    Args:
        expression: 例如 "(3.5+2)*8" 或 "2**10"。
    """
    try:
        tree = ast.parse(expression, mode="eval")
        value = _eval_node(tree)
        return f"{expression} = {value}"
    except Exception as exc:  # noqa: BLE001
        return f"计算失败：{exc}"


@tool
def current_time() -> str:
    """返回本地当前日期时间（到秒）。"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@tool
def search_notes(keyword: str) -> str:
    """
    在本地 notes 目录中按关键字搜索笔记内容。

    Args:
        keyword: 要查找的关键字。
    """
    if not NOTES_DIR.exists():
        return "notes 目录不存在。"
    hits: list[str] = []
    for path in sorted(NOTES_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if keyword.lower() in text.lower():
            # 截取首个命中行附近
            for line in text.splitlines():
                if keyword.lower() in line.lower():
                    hits.append(f"{path.name}: {line.strip()}")
                    break
    if not hits:
        return f"未找到包含「{keyword}」的笔记。"
    return "\n".join(hits[:8])


def all_tools():
    """
    返回本模块全部工具列表。

    :return: Tool 对象列表。
    """
    return [calculate, current_time, search_notes]
