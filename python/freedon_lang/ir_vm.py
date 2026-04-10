from __future__ import annotations

from typing import Any, List

from .env import Env
from .errors import EvalError
from .evaluator import Lambda, eval_expr
from .ir_ops import (
    NAME_BY_OP,
    OP_APPLY,
    OP_DEF,
    OP_JUMP,
    OP_JUMP_IF_FALSE,
    OP_LOAD,
    OP_MAKE_LAMBDA,
    OP_POP,
    OP_PUSH,
)


def run_vm(code: list[tuple], env: Env) -> Any:
    stack: list[Any] = []
    pc = 0
    n = len(code)

    while pc < n:
        inst = code[pc]
        pc += 1
        if not inst:
            continue
        op = inst[0]
        if isinstance(op, str):
            op_name = op
        else:
            op_name = NAME_BY_OP.get(int(op), "")

        if op_name == "push" or op == OP_PUSH:
            stack.append(inst[1])
        elif op_name == "load" or op == OP_LOAD:
            name = inst[1]
            stack.append(env.get(name))
        elif op_name == "apply" or op == OP_APPLY:
            argc = int(inst[1])
            if argc < 0:
                raise EvalError("apply: bad argc")
            if len(stack) < argc + 1:
                raise EvalError("apply: stack underflow")
            # 栈底 … 参数(从左到右) … 函数在栈顶
            fn = stack.pop()
            args = [stack.pop() for _ in range(argc)]
            args.reverse()
            if not callable(fn):
                raise EvalError(f"apply: not callable {fn!r}")
            stack.append(fn(*args))
        elif op_name == "jump-if-false" or op == OP_JUMP_IF_FALSE:
            target = int(inst[1])
            cond = stack.pop()
            if not cond:
                pc = target
        elif op_name == "jump" or op == OP_JUMP:
            pc = int(inst[1])
        elif op_name == "def" or op == OP_DEF:
            name = str(inst[1])
            val = stack.pop()
            env.set(name, val)
            stack.append(val)
        elif op_name == "pop" or op == OP_POP:
            stack.pop()
        elif op_name == "make-lambda" or op == OP_MAKE_LAMBDA:
            params = inst[1]
            inner = inst[2]
            if not isinstance(inner, list):
                inner = list(inner)
            stack.append(
                Lambda(
                    params=list(params),
                    body=None,
                    env=env,
                    ir_code=inner,
                )
            )
        else:
            raise EvalError(f"unknown ir op: {inst!r}")

    if len(stack) != 1:
        raise EvalError(f"vm finished with stack size {len(stack)}, expected 1")
    return stack[0]


def eval_form_via_pipeline(form: Any, env: Env) -> Any:
    """根据 pipeline 配置选择解释 / 编译 / JIT / mixed。"""
    from . import pipeline
    from .ir_compile import compile_form

    mode = pipeline.get_exec_mode()
    ir_t = pipeline.get_ir_target()

    if ir_t == 0:
        return eval_expr(form, env)

    if mode == "interp":
        return eval_expr(form, env)

    try:
        code = compile_form(form, ir_t)
        if mode == "compile":
            return run_vm(code, env)
        if mode == "jit":
            return _jit_run_cached(code, env)
        if mode == "mixed":
            try:
                return run_vm(code, env)
            except EvalError:
                return eval_expr(form, env)
    except EvalError:
        if mode == "mixed":
            return eval_expr(form, env)
        raise

    return eval_expr(form, env)


_jit_cache: dict[int, list[tuple]] = {}


def _jit_run_cached(code: list[tuple], env: Env) -> Any:
    """原型 JIT：按 bytecode 结构缓存 IR，避免重复编译遍历（非原生机器码）。"""
    key = _code_key(code)
    _jit_cache[key] = code
    return run_vm(code, env)


def _frozen(obj: Any) -> Any:
    if isinstance(obj, list):
        return tuple(_frozen(x) for x in obj)
    if isinstance(obj, tuple):
        return tuple(_frozen(x) for x in obj)
    return obj


def _code_key(code: list[tuple]) -> int:
    return hash(_frozen(code))
