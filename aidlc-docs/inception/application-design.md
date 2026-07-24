# Application Design

## 아키텍처

```
data/knowledge_base/*.md
        │  (ingest: 섹션 단위 청킹)
        ▼
app/ingest.py ──▶ sentence-transformers 임베딩 ──▶ Chroma (data/chroma, persistent)
                                                        │
질문 ──▶ app/retriever.py (질문 임베딩 → top-k 검색) ◀──┘
        │
        ▼
app/generator.py (검색된 청크를 컨텍스트로 프롬프트 구성 → Claude API 호출)
        │
        ▼
app/cli.py (질문 입력 / 답변 + 출처 출력)
```

## 모듈

| 모듈 | 역할 | 외부 의존 |
|---|---|---|
| `app/ingest.py` | 지식 저장소 로드 → 청킹 → 임베딩 → Chroma 저장 | sentence-transformers (로컬, 키 불필요) |
| `app/retriever.py` | 질문 임베딩 → 상위 k개 청크 검색 | 위와 동일 |
| `app/generator.py` | 컨텍스트 + 질문으로 프롬프트 구성 → Claude 호출 | `ANTHROPIC_API_KEY` 필요 |
| `app/cli.py` | 진입점 (ingest / ask / chat) | — |

## 청킹 전략
마크다운 `##` 섹션 단위로 분할. 섹션이 너무 길면 (기준: 문자수) 문단 단위로 추가 분할.
각 청크는 메타데이터로 `source`(파일명), `section`(헤더) 를 가진다 — 답변 시 출처 표시에 사용.

## 모델 기본값
생성 모델 기본값은 `claude-opus-5` (claude-api 스킬 기본 정책). `.env`의 `ANTHROPIC_MODEL`로 재정의 가능 —
연습/비용 절감 목적이면 `claude-sonnet-5` 또는 `claude-haiku-4-5`로 낮출 수 있음(HANDOFF.md에 안내).

## 결정 근거 (설계 판단)
- 임베딩을 로컬 모델(sentence-transformers)로 택한 이유: project-flow 계약상 "키 없이 뼈대가 e2e로 돌아야" 함.
  Voyage AI 등 임베딩 전용 API도 대안이지만 추가 키 요구 없이 검색 파이프라인을 완전히 테스트 가능하게 하려고 로컬 모델 선택.
- 벡터스토어는 Chroma(로컬 persistent) — 별도 서버/키 불필요, 소규모 지식저장소에 적합.
