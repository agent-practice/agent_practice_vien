# Audit Log

- 2026-07-25: 사용자 요청 — "상용 LLM 모델 정보 지식저장소 기반 RAG 에이전트 구축, 프로젝트 진행". 별도 승인 게이트 질문 없이 project-flow 계약(자율 진행)으로 처리하기로 판단.
  근거: 소규모 개인 연습 프로젝트, 팀/공개 배포 아님, 사용자가 이미 진행을 명시적으로 요청.
- 진행 방식 결정: Python + 로컬 임베딩(sentence-transformers) + Chroma + Claude API. 언어/스택은 되묻지 않고 RAG 생태계 표준 조합으로 직접 결정 (되물음 비용 > 이득 판단).
- 2026-07-25 (같은 날, 후속 턴): 사용자가 실제 요구를 "성능 벤치마크 참고해서 요청에 맞는 모델 추천"으로 명확히 함.
  Artificial Analysis API(무료 티어, 지능/코딩/수학 벤치마크+가격)를 WebSearch/WebFetch로 사전 조사해 실존·스펙 확인
  후 채택 — URL을 추측하지 않고 실제 조사로 검증. Ollama(qwen3:14b, 이미 로컬 설치됨) tool-calling으로 생성 백엔드
  교체, Chroma/sentence-transformers/anthropic 의존성 전부 제거. 사용자가 "일단 시작해줘"로 승인.
