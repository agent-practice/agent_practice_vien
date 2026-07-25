"""CLI 진입점.

사용법:
    python -m app.cli recommend "설명"   # 1회성 추천/질문
    python -m app.cli chat               # 대화형 반복 질문 (매 질문 독립 실행)
"""

from __future__ import annotations

import argparse

from dotenv import load_dotenv

from app.agent import recommend


def _answer_and_print(query: str) -> None:
    try:
        answer = recommend(query)
    except RuntimeError as e:
        print(f"[오류] {e}")
        return
    print(answer)


def cmd_recommend(args: argparse.Namespace) -> None:
    _answer_and_print(args.request)


def cmd_chat(args: argparse.Namespace) -> None:
    print("질문을 입력하세요 (종료: exit / quit / Ctrl-D)")
    while True:
        try:
            query = input("\n> ").strip()
        except EOFError:
            break
        if not query:
            continue
        if query.lower() in {"exit", "quit"}:
            break
        _answer_and_print(query)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-practice", description="상용 LLM 모델 추천 에이전트"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_recommend = sub.add_parser("recommend", help="요청에 맞는 모델을 추천한다")
    p_recommend.add_argument("request")
    p_recommend.set_defaults(func=cmd_recommend)

    p_chat = sub.add_parser("chat", help="대화형으로 반복 질문한다")
    p_chat.set_defaults(func=cmd_chat)

    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
