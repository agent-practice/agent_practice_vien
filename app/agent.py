"""tool-calling 루프: 로컬 지식·실시간 벤치마크를 근거로 모델 추천/질문에 답한다."""

from __future__ import annotations

import json

from app.ollama_client import chat
from app.tools import TOOL_FUNCTIONS, TOOLS_SCHEMA

SYSTEM_PROMPT = (
    "당신은 상용 LLM 모델(Claude/GPT/Gemini/Llama/Mistral/Grok) 중 사용자의 요구(용도·예산·"
    "성능 니즈)에 가장 적합한 모델을 추천하거나, 공급사·모델에 대한 질문에 답하는 에이전트입니다. "
    "숫자(벤치마크 점수, 가격)는 반드시 list_model_benchmarks 도구로, 정성적 설명은 "
    "describe_provider 도구로 확인한 뒤 답하세요. 도구 없이 추측으로 점수나 가격을 지어내지 "
    "마세요. 최종 답변에는 추천 모델과 근거(어떤 지수/가격을 근거로 했는지)를 명시하세요."
)

MAX_TOOL_ROUNDS = 5


def _call_tool(name: str, arguments: dict) -> dict:
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return {"error": f"알 수 없는 도구: {name}"}
    try:
        return fn(**arguments)
    except Exception as e:
        return {"error": f"{name} 실행 중 오류: {e}"}


def recommend(request: str, model: str | None = None) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request},
    ]

    for _ in range(MAX_TOOL_ROUNDS):
        message = chat(messages, tools=TOOLS_SCHEMA, model=model)
        tool_calls = message.get("tool_calls")
        if not tool_calls:
            return message.get("content", "")

        messages.append(message)
        for call in tool_calls:
            fn_name = call["function"]["name"]
            args = call["function"].get("arguments") or {}
            if isinstance(args, str):
                args = json.loads(args)
            result = _call_tool(fn_name, args)
            messages.append({"role": "tool", "content": json.dumps(result, ensure_ascii=False)})

    return "도구 호출 횟수 제한(5회)을 넘겨서 중단했습니다. 질문을 더 구체적으로 다시 해보세요."
