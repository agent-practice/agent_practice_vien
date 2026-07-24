# ROADMAP

## MVP
- [x] 프로젝트 스켈레톤 + aidlc-docs 설계 문서
- [x] 지식베이스 시드 문서 6종 (claude/gpt/gemini/llama/mistral/grok)
- [x] ingest/retriever/generator/cli 구현
- [x] 키 핸드오프 (scripts/setup_keys.py, docs/HANDOFF.md)
- [x] 테스트 작성 (색인+검색, 키 불필요)
- [x] 의존성 설치 + 테스트 실측 검증 (`pytest` 5 passed, `python -m app.cli ingest` 청크 42개 색인 확인)
- [ ] 실사용 검증 (ANTHROPIC_API_KEY 입력 후 질문-답변 확인) — 사용자 액션 필요
- [x] git 첫 커밋 (`feature/rag-agent-mvp` 브랜치, 6240e2e) — GitHub 원격은 아직 없음, 사용자 결정 대기

## 확장 아이디어 (이후)
- [ ] 답변에 청크 distance/score 노출 (검색 품질 확인용)
- [ ] 지식베이스 문서 추가/자동 갱신 스크립트
- [ ] 웹 UI (Streamlit/FastAPI)
- [ ] 재랭킹(rerank) 단계 추가
- [ ] 출처 하이라이트 (근거 문장 강조)
