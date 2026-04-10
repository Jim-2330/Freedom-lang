from __future__ import annotations

import math
from typing import Any, Callable

from .env import Env
from .hijack import HIJACK_REGISTRY
from .runtime_memory import GLOBAL_MEMORY
from .storage import GLOBAL_STORE
from . import pipeline
from .ir_compile import compile_form


def _wrap(name: str, fn: Callable[..., Any]) -> Callable[..., Any]:
    def inner(*args: Any, **kwargs: Any) -> Any:
        return HIJACK_REGISTRY.wrap_call(name, fn, *args, **kwargs)

    return inner


def standard_env() -> Env:
    env = Env()

    # 基础算术与比较（可被重定义）
    env.set("+", _wrap("+", lambda *xs: sum(xs)))
    env.set("-", _wrap("-", lambda x, *xs: x - sum(xs) if xs else -x))
    env.set("*", _wrap("*", lambda *xs: math.prod(xs)))

    def _div(x: Any, *xs: Any) -> Any:
        acc = x
        for v in xs:
            acc /= v
        return acc

    env.set("/", _wrap("/", _div))

    env.set("=", _wrap("=", lambda a, b: a == b))
    env.set("<", _wrap("<", lambda a, b: a < b))
    env.set(">", _wrap(">", lambda a, b: a > b))
    env.set("<=", _wrap("<=", lambda a, b: a <= b))
    env.set(">=", _wrap(">=", lambda a, b: a >= b))

    # 逻辑
    env.set("and", _wrap("and", lambda a, b: a and b))
    env.set("or", _wrap("or", lambda a, b: a or b))
    env.set("not", _wrap("not", lambda a: not a))

    # 列表
    env.set("list", _wrap("list", lambda *xs: list(xs)))
    env.set("head", _wrap("head", lambda xs: xs[0]))
    env.set("tail", _wrap("tail", lambda xs: xs[1:]))
    env.set("append", _wrap("append", lambda xs, v: xs + [v]))

    # IO
    env.set("print", _wrap("print", lambda *xs: print(*xs)))

    # 全域寻址（虚拟）
    # 推荐空间名：
    # - "ram": 内存
    # - "vram": 显存
    # - "reg": 寄存器（地址可以是名字，如 "R1"）
    env.set(
        "peek",
        _wrap("peek", lambda addr, space="ram": GLOBAL_MEMORY.peek(addr, space)),
    )
    env.set(
        "poke",
        _wrap(
            "poke",
            lambda addr, value, space="ram": GLOBAL_MEMORY.poke(addr, value, space),
        ),
    )

    # 指令劫持 API
    def _hijack(name: str, fn: Callable[..., Any]) -> None:
        HIJACK_REGISTRY.register(name, lambda inner, args, kwargs: fn(inner, *args))

    env.set("hijack", _wrap("hijack", _hijack))

    def _unhijack(name: str) -> None:
        HIJACK_REGISTRY.remove(name)

    env.set("unhijack", _wrap("unhijack", _unhijack))

    # 分布式流动（占位）
    def _migrate(target: str) -> str:
        msg = f"[migrate] 请求迁移到 {target}（Alpha: 仅记录，不实际迁移）"
        print(msg)
        return msg

    env.set("migrate", _wrap("migrate", _migrate))

    # storage（可持久化）
    env.set("store-get", _wrap("store-get", lambda key, default=None: GLOBAL_STORE.get(key, default)))
    env.set("store-set", _wrap("store-set", lambda key, value: GLOBAL_STORE.set(key, value)))
    env.set("store-load", _wrap("store-load", lambda path: GLOBAL_STORE.load(path)))
    env.set("store-save", _wrap("store-save", lambda path=None: GLOBAL_STORE.save(path)))

    # 元编程
    env.set("type", _wrap("type", lambda x: type(x).__name__))

    # 流水线：解释 / 编译 / JIT / mixed + IR 层数（0=AST 直解，1=IR1，2=IR2）
    env.set("set-exec-mode", _wrap("set-exec-mode", pipeline.set_exec_mode))
    env.set("set-ir-target", _wrap("set-ir-target", pipeline.set_ir_target))
    env.set("set-frontend", _wrap("set-frontend", pipeline.set_frontend))
    env.set("pipeline-status", _wrap("pipeline-status", lambda: pipeline.pipeline_status()))
    env.set(
        "compile-to-ir",
        _wrap("compile-to-ir", lambda expr, level: compile_form(expr, int(level))),
    )

    return env

