from pathlib import Path

from app.ingest import KNOWLEDGE_BASE_DIR, build_index, chunk_document, get_collection, load_all_chunks


def test_chunk_document_splits_sections(tmp_path: Path):
    md = tmp_path / "sample.md"
    md.write_text(
        "# Sample\n\n## 개요\n내용 A\n\n## 특징\n내용 B\n",
        encoding="utf-8",
    )
    chunks = chunk_document(md)
    sections = {c["section"] for c in chunks}
    assert "개요" in sections
    assert "특징" in sections
    assert all(c["source"] == "sample.md" for c in chunks)


def test_load_all_chunks_from_real_knowledge_base():
    chunks = load_all_chunks()
    assert len(chunks) > 0
    sources = {c["source"] for c in chunks}
    assert "claude.md" in sources
    assert "gpt.md" in sources


def test_build_index_populates_collection(tmp_path: Path):
    persist_dir = tmp_path / "chroma"

    count = build_index(knowledge_dir=KNOWLEDGE_BASE_DIR, persist_dir=persist_dir)
    assert count > 0

    collection = get_collection(persist_dir=persist_dir)
    assert collection.count() == count
