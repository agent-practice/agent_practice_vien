"""로컬 Ollama 서버와 통신하는 얇은 클라이언트.

외부 API 키 불필요 — 로컬 11434 포트의 Ollama 서버만 있으면 동작한다.
"""

from __future__ import annotations

import os

import requests

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3:14b")
REQUEST_TIMEOUT = 300


def chat(messages: list[dict], tools: list[dict] | None = None, model: str | None = None) -> dict:
    payload = {
        "model": model or DEFAULT_MODEL,
        "messages": messages,
        "stream": False,
    }
    if tools:
        payload["tools"] = tools

    try:
        resp = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=REQUEST_TIMEOUT)
    except requests.ConnectionError as e:
        raise RuntimeError(
            f"Ollama 서버({OLLAMA_HOST})에 연결할 수 없습니다. "
            "`ollama serve`가 실행 중인지, 모델이 있는지(`ollama list`) 확인하세요."
        ) from e
    resp.raise_for_status()
    return resp.json()["message"]
