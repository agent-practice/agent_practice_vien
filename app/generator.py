"""검색된 청크를 컨텍스트로 Claude API를 호출해 답변을 생성한다.

ANTHROPIC_API_KEY 필요 (docs/HANDOFF.md 참고). 기본 모델은 claude-opus-5이며
ANTHROPIC_MODEL 환경변수로 재정의할 수 있다.
"""

from __future__ import annotations

import os

import anthropic

from app.retriever import RetrievedChunk

DEFAULT_MODEL = "claude-opus-5"

SYSTEM_PROMPT = (
    "당신은 상용 LLM 모델 정보를 정리한 지식 저장소를 근거로 질문에 답하는 어시스턴트입니다. "
    "아래 제공된 컨텍스트에 있는 정보만 사용해 답하세요. 컨텍스트에 없는 내용은 "
    '"지식 저장소에 없는 정보입니다"라고 명시하고, 일반 지식으로 추측해서 단정하지 마세요. '
    "답변 끝에 참고한 출처(파일명/섹션)를 나열하세요."
)


def build_context(chunks: list[RetrievedChunk]) -> str:
    parts = []
    for i, c in enumerate(chunks, 1):
        parts.append(f"[출처 {i}: {c.source} / {c.section}]\n{c.text}")
    return "\n\n---\n\n".join(parts)


def generate_answer(
    query: str, chunks: list[RetrievedChunk], model: str | None = None
) -> str:
    if not os.environ.get("ANTHROPIC_API_KEY") and not os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        raise RuntimeError(
            "ANTHROPIC_API_KEY가 설정되지 않았습니다. "
            "`python3 scripts/setup_keys.py` 로 입력하세요 (자세한 안내: docs/HANDOFF.md)."
        )

    client = anthropic.Anthropic()
    context = build_context(chunks)
    user_content = f"[컨텍스트]\n{context}\n\n[질문]\n{query}"

    response = client.messages.create(
        model=model or os.environ.get("ANTHROPIC_MODEL", DEFAULT_MODEL),
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_content}],
    )

    if response.stop_reason == "refusal":
        return "답변이 안전 정책에 의해 거부되었습니다. 질문을 다르게 표현해 다시 시도하세요."

    text_parts = [block.text for block in response.content if block.type == "text"]
    return "\n".join(text_parts)
