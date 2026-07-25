# Requirements

## v2로 개정 (2026-07-25) — v1은 아래 "v1 (히스토리)" 참고

## 목표
사용자가 서술한 요구(용도·예산·성능)에 맞춰, 실시간 벤치마크·가격 데이터를 근거로
상용 LLM 모델(Claude, GPT, Gemini, Llama, Mistral, Grok)을 추천하는 에이전트.

## 범위 (v2 MVP)
- 생성 백엔드: Ollama로 로컬 실행하는 Qwen(qwen3:14b) — 키 불필요
- tool-calling: agent가 필요에 따라 아래 두 도구를 스스로 호출
  - `describe_provider`: 공급사 개요/특징(로컬 data/knowledge_base/*.md), 키 불필요
  - `list_model_benchmarks`: Artificial Analysis API로 지능/코딩/수학 지수·속도·가격 실시간 조회
- 인터페이스: CLI (`python -m app.cli recommend "요청"` / 대화형 `chat`)

## 범위 밖 (이후 확장 여지)
- 웹 UI, 벤치마크 응답 영속 캐시, 진짜 멀티턴 대화 히스토리, 다른 벤치마크 소스 추가

## 키 의존성
- describe_provider: 키 불필요 (로컬 파일)
- list_model_benchmarks: `ARTIFICIALANALYSIS_API_KEY` 필요 (무료 티어, scripts/setup_keys.py로 로컬 입력)
- 생성: Ollama 로컬 서버만 있으면 됨 (클라우드 API 키 불필요)

## 성공 기준
- 키 없이: describe_provider 기반 질문에 정상 답변 (에러 없이), list_model_benchmarks는 안내 메시지 반환
- 키 있으면: 실제 벤치마크 지수/가격을 근거로 든 추천 답변

---

## v1 (히스토리, 대체됨)
Chroma 벡터검색 + sentence-transformers 로컬 임베딩 + Claude API로 정적 지식베이스에 답하는 RAG.
"성능 벤치마크 참고 추천"이라는 실제 요구에는 정적 문서보다 실시간 데이터가 맞다고 판단해 v2로 전환.
