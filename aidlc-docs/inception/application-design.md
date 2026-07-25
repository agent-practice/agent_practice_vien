# Application Design (v2)

## 아키텍처

```
사용자 요청
    │
    ▼
app/agent.py (tool-calling 루프, MAX_TOOL_ROUNDS=5)
    │  chat + tools
    ▼
app/ollama_client.py ──▶ Ollama 서버 (qwen3:14b, 로컬, http://localhost:11434)
    │
    ├─ tool_call: describe_provider(provider) ──▶ app/tools.py ──▶ data/knowledge_base/*.md (읽기)
    │
    └─ tool_call: list_model_benchmarks(limit) ──▶ app/tools.py ──▶ Artificial Analysis API
                                                        (GET /api/v2/data/llms/models, x-api-key)
    │
    ▼
최종 답변 (app/cli.py 출력)
```

## 모듈

| 모듈 | 역할 | 외부 의존 |
|---|---|---|
| `app/ollama_client.py` | Ollama `/api/chat` 호출 (tools 파라미터 포함) | 로컬 Ollama 서버만 (키 불필요) |
| `app/tools.py` | tool 함수 구현 + JSON 스키마 정의 | describe_provider: 없음 / list_model_benchmarks: `ARTIFICIALANALYSIS_API_KEY` |
| `app/agent.py` | 시스템 프롬프트 + tool-calling 루프 (최대 5라운드) | 위 두 모듈 |
| `app/cli.py` | 진입점 (recommend / chat) | — |

## tool-calling 루프 동작 확인 (실측)
Ollama `/api/chat`에 `tools` 스키마를 넘기면 `message.tool_calls`에
`{"function": {"name", "arguments": {...}}}` 형태로 반환됨(arguments는 이미 dict, JSON 문자열 아님 —
OpenAI Chat Completions API와 다른 점). tool 실행 결과는 `{"role": "tool", "content": <JSON 문자열>}`로
다시 메시지에 추가해 재호출하면 그 내용을 근거로 최종 답변을 생성함 — 실제 curl 테스트로 확인.

## 설계 판단
- **벡터검색 제거**: agent가 공급사 이름으로 직접 tool-call하는 구조라 임베딩 기반 유사도 검색이 불필요.
  Chroma/sentence-transformers 의존성 전체 제거 → 설치가 훨씬 가벼워짐(torch 등 불필요).
- **정적 가격 정보 제거**: 지식베이스 문서에 있던 "가격" 섹션은 `list_model_benchmarks`의 실시간 가격과
  중복/충돌 소지가 있어 삭제. 지식베이스는 이제 정성적 정보(개요/특징/용도/접근법)만 담당.
- **Artificial Analysis API 선택**: 상용 LLM의 지능/코딩/수학 벤치마크 지수와 가격을 한 번에 제공하는
  무료 공개 API. 무료 티어는 일 100회 제한, 내부용만 허용(재배포 불가) — 개인 연습 프로젝트 용도에 부합.
  (검토했으나 채택 안 한 대안: OpenRouter 모델 목록 API — 가격/컨텍스트 정보는 있으나 지능/코딩 벤치마크
  지수가 없어서 "성능 벤치마크 참고 추천"이라는 요구에는 Artificial Analysis가 더 적합)
- **미검증 항목**: `list_model_benchmarks`는 이번 세션에 실제 API 키가 없어 라이브 호출을 실측하지 못함.
  응답 스키마는 문서 조사 기반으로 방어적으로 파싱하도록 작성(dict/list 양쪽 케이스 처리) — 사용자가
  키 입력 후 실행하면 실제 스키마와 맞는지 확인 필요.
