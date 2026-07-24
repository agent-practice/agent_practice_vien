"""지식 저장소(data/knowledge_base/*.md)를 읽어 청킹 후 Chroma에 색인한다.

키 불필요 — 로컬 임베딩 모델(sentence-transformers)만 사용한다.
"""

from __future__ import annotations

import re
from pathlib import Path

import chromadb
from chromadb.utils import embedding_functions

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = REPO_ROOT / "data" / "knowledge_base"
CHROMA_DIR = REPO_ROOT / "data" / "chroma"
COLLECTION_NAME = "llm_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MAX_CHUNK_CHARS = 1500

_SECTION_RE = re.compile(r"^##\s+(.+)$", re.MULTILINE)


def _split_sections(text: str, doc_title: str) -> list[tuple[str, str]]:
    """마크다운을 '## ' 섹션 단위로 분리한다.

    '##' 섹션이 시작되기 전 서문(주로 '# 제목' 한 줄)은 doc_title 섹션으로 묶는다.
    """
    matches = list(_SECTION_RE.finditer(text))
    if not matches:
        return [(doc_title, text.strip())]

    sections: list[tuple[str, str]] = []
    preamble = text[: matches[0].start()].strip()
    if preamble:
        sections.append((doc_title, preamble))

    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        sections.append((header, body))

    return sections


def _split_long_section(body: str, limit: int) -> list[str]:
    """섹션이 limit보다 길면 문단(빈 줄) 단위로 추가 분할한다."""
    if len(body) <= limit:
        return [body]

    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""
    for p in paragraphs:
        candidate = f"{current}\n\n{p}".strip() if current else p
        if len(candidate) > limit and current:
            chunks.append(current)
            current = p
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks or [body]


def chunk_document(path: Path) -> list[dict]:
    """파일 하나를 청크 딕셔너리 리스트로 변환한다."""
    text = path.read_text(encoding="utf-8")
    doc_title = path.stem
    chunks: list[dict] = []
    for section, body in _split_sections(text, doc_title):
        if not body:
            continue
        for part_idx, part in enumerate(_split_long_section(body, MAX_CHUNK_CHARS)):
            chunk_text = part if section == doc_title else f"## {section}\n\n{part}"
            chunks.append(
                {
                    "text": chunk_text,
                    "source": path.name,
                    "section": section,
                    "part": part_idx,
                }
            )
    return chunks


def load_all_chunks(knowledge_dir: Path = KNOWLEDGE_BASE_DIR) -> list[dict]:
    chunks: list[dict] = []
    for path in sorted(knowledge_dir.glob("*.md")):
        chunks.extend(chunk_document(path))
    return chunks


def get_client(persist_dir: Path = CHROMA_DIR):
    persist_dir.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(persist_dir))


def get_collection(client=None, persist_dir: Path = CHROMA_DIR):
    client = client or get_client(persist_dir)
    embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL
    )
    return client.get_or_create_collection(name=COLLECTION_NAME, embedding_function=embed_fn)


def build_index(
    knowledge_dir: Path = KNOWLEDGE_BASE_DIR, persist_dir: Path = CHROMA_DIR
) -> int:
    """지식 저장소를 통째로 다시 색인한다. 반환값: 색인된 청크 수."""
    client = get_client(persist_dir)
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass
    collection = get_collection(client, persist_dir)

    chunks = load_all_chunks(knowledge_dir)
    if not chunks:
        return 0

    ids = [f"{c['source']}::{c['section']}::{c['part']}" for c in chunks]
    documents = [c["text"] for c in chunks]
    metadatas = [{"source": c["source"], "section": c["section"]} for c in chunks]

    collection.add(ids=ids, documents=documents, metadatas=metadatas)
    return len(chunks)


def main() -> None:
    count = build_index()
    print(f"색인 완료: 청크 {count}개 → {CHROMA_DIR}")


if __name__ == "__main__":
    main()
