from __future__ import annotations

from typing import Any

from .builtins import standard_env
from .ir_vm import eval_form_via_pipeline
from .parser import parse
from .tokenizer import tokenize


def run_repl() -> None:
    print("Freedon Lang v0.1-Alpha REPL. Ctrl+C 退出。")
    env = standard_env()
    while True:
        try:
            line = input("freedon> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line.strip():
            continue

        try:
            tokens = tokenize(line)
            program = parse(tokens)
            result: Any = None
            for form in program.forms:
                result = eval_form_via_pipeline(form, env)
            if result is not None:
                print("=>", result)
        except Exception as exc:  # noqa: BLE001
            print("[error]", exc)

