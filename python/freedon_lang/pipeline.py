from __future__ import annotations

from typing import Literal

ExecMode = Literal["interp", "compile", "jit", "mixed"]
IrTarget = Literal[0, 1, 2]
Frontend = Literal["lisp", "line"]

_exec_mode: ExecMode = "interp"
_ir_target: IrTarget = 0
_frontend: Frontend = "lisp"


def get_exec_mode() -> ExecMode:
    return _exec_mode


def set_exec_mode(mode: str) -> str:
    global _exec_mode
    m = str(mode).lower()
    if m not in ("interp", "compile", "jit", "mixed"):
        raise ValueError(f"exec-mode must be interp|compile|jit|mixed, got {mode!r}")
    _exec_mode = m  # type: ignore[assignment]
    return _exec_mode


def get_ir_target() -> IrTarget:
    return _ir_target


def set_ir_target(level: int) -> int:
    global _ir_target
    n = int(level)
    if n not in (0, 1, 2):
        raise ValueError("ir-target must be 0, 1, or 2")
    _ir_target = n  # type: ignore[assignment]
    return _ir_target


def get_frontend() -> Frontend:
    return _frontend


def set_frontend(name: str) -> str:
    global _frontend
    n = str(name).lower()
    if n not in ("lisp", "line"):
        raise ValueError("frontend must be lisp|line")
    _frontend = n  # type: ignore[assignment]
    return _frontend


def pipeline_status() -> dict[str, str | int]:
    return {"exec-mode": _exec_mode, "ir-target": _ir_target, "frontend": _frontend}
