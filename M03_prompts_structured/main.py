"""
M03 小项目：技术文章情报卡生成器。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from M03_prompts_structured.extractor import extract_brief
from shared.config import get_chat_model, load_settings, print_settings_summary


def main(argv: list[str] | None = None) -> int:
    """
    从文件或命令行文本抽取情报卡并打印 JSON。

    :param argv: 命令行参数。
    :return: 退出码。
    """
    parser = argparse.ArgumentParser(description="技术文章情报卡生成器")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--file", type=str, help="原文文件路径")
    group.add_argument("--text", type=str, help="直接传入原文")
    args = parser.parse_args(argv)

    if args.file:
        article = Path(args.file).read_text(encoding="utf-8")
    else:
        article = args.text

    if not article.strip():
        print("原文为空。", file=sys.stderr)
        return 1

    settings = load_settings(require_api_key=True)
    print_settings_summary(settings)
    model = get_chat_model(temperature=0)

    brief = extract_brief(model, article)
    print("=== 情报卡 JSON ===")
    print(json.dumps(brief.model_dump(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
