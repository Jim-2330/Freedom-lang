from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional

from .env import Env
from .errors import EvalError
from .parser import Program, Symbol


@dataclass
class Lambda:
    params: List[str]
    body: Any
    env: Env
    ir_code: Optional[List[tuple]] = None

    def __call__(self, *args: Any) -> Any:
        if len(args) != len(self.params):
            raise EvalError(f"expected {len(self.params)} args, got {len(args)}")
        local = Env(parent=self.env)
        for name, value in zip(self.params, args, strict=False):
            local.set(name, value)
        if self.ir_code is not None:
            from .ir_vm import run_vm

            return run_vm(self.ir_code, local)
        return eval_expr(self.body, local)


def eval_program(program: Program, env: Env) -> Any:
    from .ir_vm import eval_form_via_pipeline

    result = None
    for form in program.forms:
        result = eval_form_via_pipeline(form, env)
    return result


def eval_expr(expr: Any, env: Env) -> Any:
    # 原子
    if isinstance(expr, Symbol):
        return env.get(expr)
    if isinstance(expr, (int, float, str, bool)):
        return expr

    if not isinstance(expr, list):
        return expr

    if not expr:
        return None

    head, *tail = expr

    # 特殊形式
    if isinstance(head, Symbol):
        if head == "quote":
            (value,) = tail
            return value
        if head == "do":
            result = None
            for form in tail:
                result = eval_expr(form, env)
            return result
        if head == "if":
            test, conseq, alt = tail
            branch = conseq if eval_expr(test, env) else alt
            return eval_expr(branch, env)
        if head == "def":
            name, value_expr = tail
            if not isinstance(name, Symbol):
                raise EvalError("def: first argument must be a symbol")
            value = eval_expr(value_expr, env)
            env.set(name, value)
            return value
        if head == "fn":
            if len(tail) < 2:
                raise EvalError("fn: expected (fn (params...) body...)")
            params_expr, *body_exprs = tail
            if not isinstance(params_expr, list) or not all(
                isinstance(p, Symbol) for p in params_expr
            ):
                raise EvalError("fn: parameter list must be list of symbols")
            params = [str(p) for p in params_expr]
            body = body_exprs[0] if len(body_exprs) == 1 else [Symbol("do"), *body_exprs]
            return Lambda(params=params, body=body, env=env, ir_code=None)

    # 函数调用
    fn = eval_expr(head, env)
    args = [eval_expr(arg, env) for arg in tail]

    if callable(fn):
        return fn(*args)
    raise EvalError(f"attempted to call non-callable: {fn!r}")

