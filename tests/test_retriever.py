from pathlib import Path

import pytest

from app.ingest import build_index
from app.retriever import retrieve


@pytest.fixture(scope="module")
def indexed_dir(tmp_path_factory) -> Path:
    persist_dir = tmp_path_factory.mktemp("chroma")
    build_index(persist_dir=persist_dir)
    return persist_dir


def test_retrieve_returns_relevant_chunk(indexed_dir: Path):
    results = retrieve("Claude Opus 5는 어떤 모델이야?", k=3, persist_dir=indexed_dir)
    assert results
    sources = {r.source for r in results}
    assert "anthropic-claude.md" in sources


def test_retrieve_raises_when_not_indexed(tmp_path: Path):
    with pytest.raises(RuntimeError):
        retrieve("아무 질문", persist_dir=tmp_path / "empty_chroma")
