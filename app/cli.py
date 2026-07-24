"""CLI 진입점.

사용법:
    python -m app.cli ingest          # 지식 저장소 색인 (키 불필요)
    python -m app.cli ask "질문"       # 1회성 질문 (ANTHROPIC_API_KEY 필요)
    python -m app.cli chat            # 대화형 반복 질문
"""

from __future__ import annotations

import argparse

from dotenv import load_dotenv

from app.generator import generate_answer
from app.ingest import CHROMA_DIR, build_index
from app.retriever import retrieve


def cmd_ingest(args: argparse.Namespace) -> None:
    count = build_index()
    print(f"색인 완료: 청크 {count}개 → {CHROMA_DIR}")


def _answer_and_print(query: str, k: int) -> None:
    try:
        chunks = retrieve(query, k=k)
    except RuntimeError as e:
        print(f"[오류] {e}")
        return
    try:
        answer = generate_answer(query, chunks)
    except RuntimeError as e:
        print(f"[오류] {e}")
        return
    print(answer)


def cmd_ask(args: argparse.Namespace) -> None:
    _answer_and_print(args.question, args.k)


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
        _answer_and_print(query, args.k)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-rag-agent", description="상용 LLM 지식 RAG 에이전트"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="지식 저장소를 색인한다")
    p_ingest.set_defaults(func=cmd_ingest)

    p_ask = sub.add_parser("ask", help="질문 1개에 답한다")
    p_ask.add_argument("question")
    p_ask.add_argument("-k", type=int, default=4, help="검색할 청크 수 (기본 4)")
    p_ask.set_defaults(func=cmd_ask)

    p_chat = sub.add_parser("chat", help="대화형으로 반복 질문한다")
    p_chat.add_argument("-k", type=int, default=4, help="검색할 청크 수 (기본 4)")
    p_chat.set_defaults(func=cmd_chat)

    return parser


def main() -> None:
    load_dotenv()
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
