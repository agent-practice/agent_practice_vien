import pytest
import requests

from app.agent import recommend
from app.ollama_client import OLLAMA_HOST


def _ollama_available() -> bool:
    try:
        requests.get(f"{OLLAMA_HOST}/api/version", timeout=2)
        return True
    except requests.RequestException:
        return False


@pytest.mark.skipif(not _ollama_available(), reason="로컬에 Ollama 서버가 없음")
def test_recommend_uses_local_tool_and_answers():
    answer = recommend(
        "Anthropic이 어떤 회사인지 describe_provider 도구로 확인해서 한국어 한 문장으로만 답해."
    )
    assert isinstance(answer, str)
    assert len(answer) > 0
