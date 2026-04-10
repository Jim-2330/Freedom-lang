from __future__ import annotations

from typing import Any, List

from .errors import EvalError
from .parser import Symbol


def compile_form(expr: Any, ir_level: int) -> list[tuple]:
    """将单个顶层表达式编译为 IR1 指令列表；ir_level 2 时再经 ir1_to_ir2。"""
    code: list[tuple] = []
    _compile_expr(expr, code)
    if ir_level >= 2:
        from .ir_ops import ir1_to_ir2

        return ir1_to_ir2(code)
    return code


def compile_lambda_body(body: Any, ir_level: int) -> list[tuple]:
    return compile_form(body, ir_level)


def _compile_expr(expr: Any, code: list[tuple]) -> None:
    if isinstance(expr, Symbol):
        code.append(("load", str(expr)))
        return
    if isinstance(expr, (int, float, str, bool)):
        code.append(("push", expr))
        return
    if not isinstance(expr, list):
        code.append(("push", expr))
        return
    if not expr:
        code.append(("push", None))
        return

    head, *tail = expr
    if not isinstance(head, Symbol):
        _compile_expr(head, code)
        for arg in tail:
            _compile_expr(arg, code)
        code.append(("apply", len(tail)))
        return

    h = str(head)
    if h == "quote":
        (value,) = tail
        code.append(("push", value))
        return
    if h == "do":
        for form in tail:
            _compile_expr(form, code)
            if form is not tail[-1]:
                code.append(("pop",))
        return
    if h == "if":
        test, conseq, alt = tail
        _compile_expr(test, code)
        jmp_false_idx = len(code)
        code.append(("jump-if-false", -1))
        _compile_expr(conseq, code)
        jmp_end_idx = len(code)
        code.append(("jump", -1))
        alt_start = len(code)
        code[jmp_false_idx] = ("jump-if-false", alt_start)
        _compile_expr(alt, code)
        end = len(code)
        code[jmp_end_idx] = ("jump", end)
        return
    if h == "def":
        name, value_expr = tail
        if not isinstance(name, Symbol):
            raise EvalError("def: first argument must be a symbol")
        _compile_expr(value_expr, code)
        code.append(("def", str(name)))
        return
    if h == "fn":
        if len(tail) < 2:
            raise EvalError("fn: expected (fn (params...) body...)")
        params_expr, *body_exprs = tail
        if not isinstance(params_expr, list) or not all(isinstance(p, Symbol) for p in params_expr):
            raise EvalError("fn: parameter list must be list of symbols")
        params = [str(p) for p in params_expr]
        body = body_exprs[0] if len(body_exprs) == 1 else [Symbol("do"), *body_exprs]
        inner: List[tuple] = []
        _compile_expr(body, inner)
        code.append(("make-lambda", params, inner))
        return
    for arg in tail:
        _compile_expr(arg, code)
    _compile_expr(head, code)
    code.append(("apply", len(tail)))
