"""
从原文抽取 NewsBrief 的管线。
"""

from __future__ import annotations

from langchain_core.prompts import ChatPromptTemplate

from M03_prompts_structured.schemas import NewsBrief


def build_extractor(model):
    """
    组装「提示模板 + 结构化输出」链。

    :param model: 基础聊天模型。
    :return: 可 invoke({"article": ...}) 的 runnable。
    """
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "你是技术内容分析师。根据用户给出的原文，生成结构化情报卡。"
                "只依据原文，不要编造原文没有的事实。使用中文填写字段。",
            ),
            (
                "human",
                "请分析以下文章并输出情报卡：\n\n{article}",
            ),
        ]
    )
    structured_model = model.with_structured_output(NewsBrief)
    return prompt | structured_model


def extract_brief(model, article: str) -> NewsBrief:
    """
    对单篇文章执行抽取。

    :param model: 聊天模型。
    :param article: 原文。
    :return: 校验后的 NewsBrief。
    """
    chain = build_extractor(model)
    result = chain.invoke({"article": article.strip()})
    if isinstance(result, NewsBrief):
        return result
    # 兼容少数实现返回 dict 的情况
    return NewsBrief.model_validate(result)
