"""색인된 지식 저장소에서 질문과 관련된 청크를 검색한다. 키 불필요."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.ingest import CHROMA_DIR, get_collection


@dataclass
class RetrievedChunk:
    text: str
    source: str
    section: str
    distance: float


def retrieve(query: str, k: int = 4, persist_dir: Path = CHROMA_DIR) -> list[RetrievedChunk]:
    collection = get_collection(persist_dir=persist_dir)
    if collection.count() == 0:
        raise RuntimeError(
            "색인된 데이터가 없습니다. 먼저 `python -m app.ingest` 를 실행하세요."
        )

    result = collection.query(query_texts=[query], n_results=min(k, collection.count()))

    chunks: list[RetrievedChunk] = []
    documents = result["documents"][0]
    metadatas = result["metadatas"][0]
    distances = result["distances"][0]
    for text, meta, dist in zip(documents, metadatas, distances):
        chunks.append(
            RetrievedChunk(
                text=text,
                source=meta.get("source", "unknown"),
                section=meta.get("section", ""),
                distance=dist,
            )
        )
    return chunks
