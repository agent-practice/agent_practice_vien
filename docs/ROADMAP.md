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
- [x] ARTIFICIALANALYSIS_API_KEY 입력 후 실제 벤치마크 근거 추천 확인 — 실제 라이브 API 호출 성공,
  실제 모델(GPT-5.6 Terra/Sol/Luna 등) 지능/코딩 지수·가격으로 추천 답변 생성 확인. 응답 스키마 파싱 정상 동작.
  다만 최초 호출(모델 콜드로드+긴 thinking)에 최대 5분 가까이 걸림 → `ollama_client.py` 타임아웃 180→300s로 상향.
  system prompt에 "항상 한국어로 답변" 명시 추가(첫 실측 시 영어로 답변한 것 확인해 수정).
- [x] GitHub 커밋/push + PR + 머지 (personal + org 양쪽) — org는 히스토리 분기로 merge conflict 발생,
  `git merge -X theirs` 로컬 해소 후 push로 정리 (force-push 없이)

## 확장 아이디어 (이후)
- [ ] 벤치마크 캐시를 파일 기반으로 영속화 (현재는 프로세스 메모리 캐시라 CLI 재실행마다 초기화)
- [ ] 첫 호출 지연(콜드로드+thinking, 최대 5분) 개선 — `think: false` 옵션 검토 또는 진행 상태 출력
- [ ] 웹 UI (Streamlit/FastAPI)
- [ ] 대화 히스토리 유지되는 진짜 멀티턴 chat (현재 chat은 질문마다 독립 실행)
