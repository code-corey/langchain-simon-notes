"""
从本地 Markdown 构建内存向量索引。
"""

from __future__ import annotations

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_markdown_documents(data_dir: Path | None = None) -> list[Document]:
    """
    读取目录下全部 Markdown 为 Document 列表。

    :param data_dir: 知识库目录，默认使用模块内 data/。
    :return: Document 列表。
    """
    root = data_dir or DATA_DIR
    docs: list[Document] = []
    for path in sorted(root.glob("*.md")):
        docs.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name},
            )
        )
    return docs


def build_vector_store(embeddings, *, chunk_size: int = 400, chunk_overlap: int = 80):
    """
    切分文档、向量化并写入 InMemoryVectorStore。

    :param embeddings: Embedding 模型。
    :param chunk_size: 块大小。
    :param chunk_overlap: 重叠大小。
    :return: 已索引的向量库。
    """
    docs = load_markdown_documents()
    if not docs:
        raise FileNotFoundError(f"知识库为空：{DATA_DIR}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )
    splits = splitter.split_documents(docs)
    store = InMemoryVectorStore(embedding=embeddings)
    store.add_documents(documents=splits)
    return store
