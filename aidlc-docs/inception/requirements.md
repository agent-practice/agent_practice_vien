# Requirements

## 목표
상용 LLM 모델(Claude, GPT, Gemini, Llama, Mistral, Grok 등) 정보를 담은 로컬 지식 저장소를 만들고,
사용자 질문에 그 저장소에서 근거를 찾아 답하는 RAG 에이전트를 구축한다.

## 범위 (MVP)
- 지식 저장소: `data/knowledge_base/*.md` — 모델별 개요/특징 문서 (시드 콘텐츠, 편집 가능)
- 색인: 문서를 섹션 단위로 청크 → 로컬 임베딩 모델로 벡터화 → Chroma에 저장
- 검색: 질문 임베딩 → 상위 k개 청크 검색
- 생성: 검색된 청크를 컨텍스트로 Claude API 호출 → 답변 생성
- 인터페이스: CLI (`python -m app.cli ask "질문"` / 대화형 `chat` 모드)

## 범위 밖 (이후 확장 여지)
- 웹 UI, 다중 사용자, 문서 자동 크롤링/갱신, 재랭킹, 출처 하이라이트 고도화

## 키 의존성
- 임베딩/검색: 키 불필요 (로컬 sentence-transformers)
- 생성: `ANTHROPIC_API_KEY` 필요 (scripts/setup_keys.py로 로컬 입력)

## 성공 기준
- 키 없이: 색인 생성 + 검색이 테스트로 검증됨 (e2e, mock 없이 로컬로 동작)
- 키 있으면: 질문 → 검색된 근거 기반 답변이 출처(파일명/섹션)와 함께 나옴
