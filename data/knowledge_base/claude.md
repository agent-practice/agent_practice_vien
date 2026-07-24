# Claude (Anthropic)

## 개요
Anthropic이 개발한 상용 LLM 패밀리. 안전성(헌법적 AI, Constitutional AI)과 에이전틱 코딩/장시간 자율 작업에 강점을 가진 모델 라인업.

## 주요 모델 라인업 (2026년 기준)
- **Claude Fable 5** — Anthropic 최상위 모델. 가장 어려운 추론·장시간 에이전틱 작업용. 사고(thinking)가 항상 켜져 있고, 원본 사고 과정은 노출되지 않는다(요약만 제공).
- **Claude Mythos 5** — Fable 5와 동일한 성능·가격이지만 Project Glasswing 참여자 전용 모델.
- **Claude Opus 5** — 복잡한 에이전틱 코딩과 엔터프라이즈 작업용 최신 Opus. Opus 4.8 대비 절반 가격의 Fable 5급 추론 성능.
- **Claude Sonnet 5** — 속도와 지능의 균형이 가장 좋은 라인. 코딩·에이전틱 작업에서 Opus급 품질에 근접.
- **Claude Haiku 4.5** — 가장 빠르고 저렴한 모델. 단순 작업/고속 응답에 적합.

## 특징
- 최대 1M 토큰 컨텍스트 윈도우 (Opus 5, Sonnet 5, Fable 5 등 최신 모델 기준), 최대 출력 128K 토큰.
- Adaptive Thinking: 모델이 스스로 언제·얼마나 사고할지 결정 (`thinking: {type: "adaptive"}`).
- Effort 파라미터로 사고 깊이·비용 조절 (`low`~`max`).
- 서버사이드 도구 지원: 웹 검색, 웹 페치, 코드 실행 등.
- Managed Agents: Anthropic이 에이전트 루프와 실행 샌드박스까지 호스팅하는 별도 플랫폼.

## 가격 (참고치, 확인 필요)
- Claude Opus 5: 입력 $5 / 출력 $25 (백만 토큰당)
- Claude Sonnet 5: 입력 $3 / 출력 $15 (백만 토큰당, 2026-08-31까지 인트로 할인)
- Claude Haiku 4.5: 입력 $1 / 출력 $5 (백만 토큰당)
- Claude Fable 5 / Mythos 5: 입력 $10 / 출력 $50 (백만 토큰당)

## 적합한 용도
장시간 자율 코딩 에이전트, 복잡한 멀티스텝 추론, 안전성이 중요한 엔터프라이즈 워크로드.

## 접근 방법
Claude API(Anthropic 직접), Amazon Bedrock, Google Cloud Vertex AI, Microsoft Foundry, Claude Platform on AWS를 통해 사용 가능.
