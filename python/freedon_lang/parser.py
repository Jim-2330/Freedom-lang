from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Sequence

from .errors import ParseError


Expression = Any


@dataclass
class Program:
    forms: List[Expression]


def parse(tokens: Sequence[str]) -> Program:
    """Parse token list into a Program (Lisp S-Exp AST)."""

    index = 0

    def peek() -> str | None:
        nonlocal index
        return tokens[index] if index < len(tokens) else None

    def consume_expected(expected: str) -> None:
        nonlocal index
        if peek() != expected:
            raise ParseError(f"expected '{expected}', got '{peek()}'")
        index += 1

    def parse_atom(token: str) -> Expression:
        # number (int or float)
        try:
            if "." in token:
                return float(token)
            return int(token)
        except ValueError:
            pass

        # string
        if token.startswith('"') and token.endswith('"') and len(token) >= 2:
            return bytes(token[1:-1], "utf-8").decode("unicode_escape")

        # symbol
        return Symbol(token)

    def parse_list() -> List[Expression]:
        nonlocal index
        consume_expected("(")
        result: List[Expression] = []
        while True:
            tok = peek()
            if tok is None:
                raise ParseError("unexpected EOF while reading list")
            if tok == ")":
                index += 1
                return result
            result.append(parse_expr())

    def parse_expr() -> Expression:
        nonlocal index
        tok = peek()
        if tok is None:
            raise ParseError("unexpected EOF")
        if tok == "(":
            return parse_list()
        if tok == ")":
            raise ParseError("unexpected ')'")
        index += 1
        return parse_atom(tok)

    forms: List[Expression] = []
    while peek() is not None:
        forms.append(parse_expr())

    return Program(forms=forms)


class Symbol(str):
    """Distinct type for identifiers so we can distinguish from strings."""

    pass

