# GPT (OpenAI)

## 개요
OpenAI가 개발한 상용 LLM 패밀리. ChatGPT 서비스와 API(Responses API / Chat Completions API)로 제공되며,
범용 대화, 코딩, 멀티모달(텍스트·이미지·음성) 작업에 폭넓게 쓰인다.

## 주요 모델 라인업 (일반 지식 기준 — 최신 라인업은 platform.openai.com/docs/models에서 확인 필요)
- **GPT-5 계열** — OpenAI 최신 세대 플래그십. 추론(reasoning) 강화 변형과 경량 변형을 함께 제공하는 구조(예: mini/nano급 저비용 버전).
- **o-시리즈(추론 특화 모델)** — 사고 사슬을 내부적으로 거쳐 복잡한 수학/코딩 문제에 강점을 보이는 추론 전용 라인.
- **GPT-4o 계열** — 텍스트·이미지·오디오를 함께 다루는 멀티모달 모델. 실시간 음성 대화(Realtime API)에도 사용.

## 특징
- Responses API로 도구 사용(함수 호출), 파일 검색, 코드 인터프리터, 웹 브라우징 등을 통합 제공.
- 구조화된 출력(Structured Outputs)으로 JSON 스키마 강제 가능.
- Assistants/Agents 계열 API로 상태 유지형 에이전트 구성 지원.
- Batch API로 비동기 대량 처리 시 할인 가격 제공.

## 적합한 용도
범용 챗봇, 멀티모달 애플리케이션(이미지/음성 포함), 폭넓은 서드파티 생태계(플러그인, GPTs)를 활용하는 제품.

## 접근 방법
OpenAI API 직접, Microsoft Azure OpenAI Service, ChatGPT Enterprise를 통해 사용 가능.

> 이 문서는 예시 시드 콘텐츠. 실제 배포된 최신 모델명·가격은 변동이 빠르므로 사용 전 공식 문서로 교차 확인 권장.
