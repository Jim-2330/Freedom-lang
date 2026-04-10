"""
Freedon Lang v0.1-Alpha

Lisp 核心 + 现代能力原型：
- 全域寻址（虚拟内存表）
- 逻辑重塑（符号可重绑定）
- 指令劫持（调用钩子）
- 分布式流动（占位实现）
"""

from .repl import run_repl
from .runner import run_file

__all__ = ["run_repl", "run_file"]

