# 키 핸드오프

키는 채팅으로 전달하지 않는다. 아래 절차로 본인 터미널에서 직접 입력한다.

## Ollama (로컬 실행, 키 불필요)

1. https://ollama.com 에서 설치 (또는 `brew install ollama`)
2. 모델 받기: `ollama pull qwen3:14b` (다른 Qwen 모델을 쓰려면 `.env`의 `OLLAMA_MODEL` 값을 바꾼다)
3. 서버 실행 확인: `ollama serve` (백그라운드 서비스로 이미 떠 있으면 생략)

## ARTIFICIALANALYSIS_API_KEY (벤치마크/가격 조회, 무료 티어)

1. https://artificialanalysis.ai/api-key-management-redirect 접속 (로그인/가입 후 자동으로 키 관리 페이지로 이동)
2. 키 생성 → 복사
3. 레포 루트에서:
   ```bash
   cd ~/MyProjects/agent_practice
   python3 scripts/setup_keys.py
   ```
4. 프롬프트에 키 붙여넣기 (화면에 표시 안 됨) → `.env`에 저장됨

무료 티어는 하루 100회 제한. 이 키가 없으면 `describe_provider`(로컬 지식 저장소) 도구는 그대로 동작하고,
`list_model_benchmarks`(실시간 벤치마크/가격) 도구만 안내 메시지를 반환한다 — 에러로 죽지 않는다.

## 확인

```bash
cd ~/MyProjects/agent_practice
python -m app.cli recommend "코드리뷰용 에이전트에 쓸 모델 추천해줘, 예산은 아끼고 싶어"
```
