"""agent가 tool-call로 호출하는 함수들과 그 JSON 스키마.

- describe_provider: 로컬 지식 저장소(data/knowledge_base) 조회 — 키/네트워크 불필요.
- list_model_benchmarks: Artificial Analysis API로 실시간 벤치마크/가격 조회 — ARTIFICIALANALYSIS_API_KEY 필요.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import requests

REPO_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_BASE_DIR = REPO_ROOT / "data" / "knowledge_base"

PROVIDER_FILES = {
    "anthropic": "anthropic-claude.md",
    "openai": "gpt.md",
    "google": "gemini.md",
    "meta": "llama.md",
    "mistral": "mistral.md",
    "xai": "grok.md",
}

AA_BASE_URL = "https://artificialanalysis.ai/api/v2"
_CACHE_TTL = 600
_cache: dict = {"data": None, "ts": 0.0}


def describe_provider(provider: str) -> dict:
    filename = PROVIDER_FILES.get(provider.lower())
    if not filename:
        return {
            "error": f"알 수 없는 provider: {provider}. 가능한 값: {sorted(PROVIDER_FILES)}"
        }
    path = KNOWLEDGE_BASE_DIR / filename
    if not path.exists():
        return {"error": f"지식 저장소 파일 없음: {filename}"}
    return {"provider": provider, "content": path.read_text(encoding="utf-8")}


def list_model_benchmarks(limit: int = 20) -> dict:
    api_key = os.environ.get("ARTIFICIALANALYSIS_API_KEY")
    if not api_key:
        return {
            "error": (
                "ARTIFICIALANALYSIS_API_KEY가 설정되지 않았습니다. "
                "`python3 scripts/setup_keys.py` 로 입력하세요 (자세한 안내: docs/HANDOFF.md)."
            )
        }

    now = time.time()
    if _cache["data"] is None or now - _cache["ts"] > _CACHE_TTL:
        resp = requests.get(
            f"{AA_BASE_URL}/data/llms/models",
            headers={"x-api-key": api_key},
            timeout=30,
        )
        resp.raise_for_status()
        _cache["data"] = resp.json()
        _cache["ts"] = now

    payload = _cache["data"]
    if isinstance(payload, dict):
        models = payload.get("data") or payload.get("models") or payload.get("results") or []
    else:
        models = payload

    return {"models": models[:limit]}


TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "describe_provider",
            "description": (
                "특정 LLM 공급사의 개요·특징·적합한 용도 등 정성적 정보를 "
                "로컬 지식 저장소에서 조회한다."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "provider": {
                        "type": "string",
                        "enum": sorted(PROVIDER_FILES.keys()),
                        "description": "조회할 공급사",
                    }
                },
                "required": ["provider"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_model_benchmarks",
            "description": (
                "Artificial Analysis API로 상용 LLM 모델의 실시간 지능/코딩/수학 벤치마크 지수, "
                "속도, 가격 데이터를 조회한다. 모델 추천 시 반드시 이 도구로 실제 수치를 확인할 것."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "반환할 최대 모델 수 (기본 20)",
                    }
                },
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "describe_provider": describe_provider,
    "list_model_benchmarks": list_model_benchmarks,
}
