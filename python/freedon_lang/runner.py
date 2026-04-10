from __future__ import annotations

from pathlib import Path
from typing import Any

from .builtins import standard_env
from .evaluator import eval_program
from .frontend import parse_source
from . import pipeline


def run_source(source: str, *, filename: str | None = None) -> Any:
    frontend = _detect_frontend_directive(source) or pipeline.get_frontend()
    program = parse_source(source, frontend=frontend)
    env = standard_env()
    return eval_program(program, env)


def run_file(path: str | Path) -> Any:
    path = Path(path)
    source = path.read_text(encoding="utf-8")
    return run_source(source, filename=str(path))


def _detect_frontend_directive(source: str) -> str | None:
    """支持在文件开头用一行指令选择语法前端。

    例如：
      #!frontend line
      #!frontend lisp
    """

    for raw in source.splitlines()[:20]:
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#!frontend"):
            parts = line.split()
            if len(parts) >= 2:
                return parts[1].strip()
        # 遇到第一条非指令内容就停止（避免误识别）
        break
    return None

