# AI-DLC State

- Workspace: greenfield (신규 프로젝트)
- 적용 방식: AI-DLC 핵심 원칙(설계 먼저/기능·리팩터링 분리/검증 정직 보고) + project-flow 계약(뼈대 우선 자율 진행, 승인 게이트 최소화)을 함께 적용.
  이유: 소규모 개인 연습 프로젝트, 사용자가 이미 "진행" 요청 — AI-DLC의 Adaptive Workflow Principle(작업 규모에 맞게 절차 조정)에 따름.
- 현재 단계: Construction (v2 — RAG에서 벤치마크 기반 추천 agent로 아키텍처 전환 완료, 실사용 검증 대기)
- v1(RAG, Chroma+Claude API) → v2(Ollama tool-calling agent) 전환: 사용자가 "성능 벤치마크 참고 추천"을
  실제 요구로 명확히 함에 따라 결정. 상세 근거는 `inception/application-design.md` 참고.
- 다음 단계: 사용자가 ARTIFICIALANALYSIS_API_KEY 입력 후 실제 벤치마크 근거 추천 확인
