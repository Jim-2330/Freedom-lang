from __future__ import annotations

from typing import List


def tokenize(source: str) -> List[str]:
    """Tokenize a simple Lisp-like syntax into a flat token list.

    - 支持 ; 开头的单行注释
    - 将括号、字符串、符号、数字分离
    """

    tokens: List[str] = []
    current = []
    in_string = False
    escape = False

    def flush_current() -> None:
        nonlocal current
        if current:
            tokens.append("".join(current))
            current = []

    i = 0
    n = len(source)
    while i < n:
        ch = source[i]
        if in_string:
            if escape:
                current.append(ch)
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                current.append(ch)
                flush_current()
                in_string = False
            else:
                current.append(ch)
            i += 1
            continue

        if ch == ";":
            # 注释：丢弃直到行尾
            flush_current()
            while i < n and source[i] not in ("\n", "\r"):
                i += 1
        elif ch in ("(", ")"):
            flush_current()
            tokens.append(ch)
        elif ch in (" ", "\t", "\n", "\r"):
            flush_current()
        elif ch == '"':
            flush_current()
            in_string = True
            current.append(ch)
        else:
            current.append(ch)

        i += 1
    flush_current()
    return tokens

