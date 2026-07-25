# ROADMAP

## v1 — RAG MVP (완료, v2로 대체됨)
- [x] 프로젝트 스켈레톤 + aidlc-docs 설계 문서
- [x] 지식베이스 시드 문서 6종 (claude/gpt/gemini/llama/mistral/grok)
- [x] ingest/retriever/generator/cli 구현 (Chroma + sentence-transformers + Claude API)
- [x] 키 핸드오프, 테스트, GitHub repo 2곳 생성 + push + PR + 머지
- [x] claude.md → anthropic-claude.md 파일명 수정 (macOS 대소문자 무시로 CLAUDE.md 오인식 버그)

## v2 — 벤치마크 기반 추천 agent (진행 중)
- [x] Chroma/임베딩/Claude API 제거 → Ollama(qwen3:14b) tool-calling agent로 교체
- [x] `describe_provider` 도구 (로컬 지식 저장소, 키 불필요)
- [x] `list_model_benchmarks` 도구 (Artificial Analysis API, 무료 티어 키 필요)
- [x] 지식베이스에서 정적 가격 섹션 제거 (실시간 벤치마크 도구와 중복/충돌 방지)
- [x] 키 핸드오프 갱신 (scripts/setup_keys.py, docs/HANDOFF.md → ARTIFICIALANALYSIS_API_KEY)
- [x] 테스트 4개 통과 (`describe_provider`, `list_model_benchmarks` 키 없을 때 처리, 실제 Ollama 연동 통합 테스트)
- [x] 실제 CLI 실행 확인 (`recommend` — 벤치마크 키 없이도 안내 메시지 + 대안 답변, 에러로 안 죽음)
- [ ] ARTIFICIALANALYSIS_API_KEY 입력 후 실제 벤치마크 근거 추천 확인 — 사용자 액션 필요
- [ ] GitHub 커밋/push (personal + org 양쪽 동기화)

## 확장 아이디어 (이후)
- [ ] `list_model_benchmarks` 응답 스키마 실제 키로 검증 (현재는 문서 기반 방어적 파싱만 확인, 실API 응답 미검증)
- [ ] 벤치마크 캐시를 파일 기반으로 영속화 (현재는 프로세스 메모리 캐시라 CLI 재실행마다 초기화)
- [ ] 웹 UI (Streamlit/FastAPI)
- [ ] 대화 히스토리 유지되는 진짜 멀티턴 chat (현재 chat은 질문마다 독립 실행)
