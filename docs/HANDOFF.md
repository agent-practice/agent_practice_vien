# 키 핸드오프

키는 채팅으로 전달하지 않는다. 아래 절차로 본인 터미널에서 직접 입력한다.

## ANTHROPIC_API_KEY

1. https://console.anthropic.com/settings/keys 접속 (Anthropic 계정 로그인)
2. `Create Key` → 키 복사
3. 레포 루트에서:
   ```bash
   cd ~/MyProjects/agent_practice
   python3 scripts/setup_keys.py
   ```
4. 프롬프트에 키 붙여넣기 (화면에 표시 안 됨) → `.env`에 저장됨

## 모델 변경 (선택)

기본 모델은 `claude-opus-5`. 연습/비용 절감 목적이면 `.env`의 `ANTHROPIC_MODEL`을
`claude-sonnet-5` 또는 `claude-haiku-4-5`로 바꿔도 된다.

## 확인

```bash
cd ~/MyProjects/agent_practice
python -m app.cli ingest        # 색인 (키 불필요, 첫 실행 시 임베딩 모델 ~80MB 다운로드)
python -m app.cli ask "Claude Opus 5는 어떤 모델이야?"
```

키가 없으면 `ask` 단계에서 안내 메시지와 함께 안전하게 멈춘다 (에러로 죽지 않음).
