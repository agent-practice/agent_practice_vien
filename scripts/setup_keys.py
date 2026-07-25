#!/usr/bin/env python3
"""API 키를 로컬 .env에 안전하게 저장하는 스크립트.

사용법 (레포 루트에서):
    python3 scripts/setup_keys.py

키는 화면에 표시되지 않고, .env 파일에만 저장된다 (.env는 gitignore됨).
발급 방법은 docs/HANDOFF.md 참고.
"""

from __future__ import annotations

import getpass
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

KEYS = [
    ("ARTIFICIALANALYSIS_API_KEY", "Artificial Analysis 벤치마크/가격 API (무료 티어, 일 100회 제한)"),
]

DEFAULTS = {
    "OLLAMA_MODEL": "qwen3:14b",
    "OLLAMA_HOST": "http://localhost:11434",
}


def load_env() -> dict[str, str]:
    env: dict[str, str] = {}
    if ENV_PATH.exists():
        for line in ENV_PATH.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip()
    return env


def main() -> None:
    env = load_env()
    print(f".env 위치: {ENV_PATH}\n키를 비워두면 기존 값 유지. 발급법: docs/HANDOFF.md\n")

    for key, desc in KEYS:
        status = "설정됨" if env.get(key) else "없음"
        value = getpass.getpass(f"{key} ({desc}) [현재: {status}]: ").strip()
        if value:
            env[key] = value

    for key, default in DEFAULTS.items():
        env.setdefault(key, default)

    ENV_PATH.write_text("".join(f"{k}={v}\n" for k, v in env.items()))
    ENV_PATH.chmod(0o600)
    print(f"\n저장 완료: {ENV_PATH}")
    for key, _ in KEYS:
        print(f"  {key}: {'✅' if env.get(key) else '—'}")


if __name__ == "__main__":
    main()
