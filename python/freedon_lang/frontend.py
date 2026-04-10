from __future__ import annotations

from typing import List

from .parser import Program, Symbol, parse as parse_lisp_tokens
from .tokenizer import tokenize


def parse_source(source: str, *, frontend: str = "lisp") -> Program:
    f = str(frontend).lower()
    if f == "lisp":
        return parse_lisp_tokens(tokenize(source))
    if f == "line":
        return parse_line_syntax(source)
    raise ValueError(f"unknown frontend: {frontend!r}")


def parse_line_syntax(source: str) -> Program:
    """一个“现代皮肤”示例：行式语法（非常轻量）。

    每一行是一条调用：`name arg1 arg2 ...`
    - 字符串用引号：print \"hello\"
    - 注释：以 ; 或 # 开头（或行内出现后到行尾）
    - 产出的 AST 仍然是 Lisp 的 list 形式：[Symbol(name), ...args]
    """

    # 方案：把每一行“包装成一对括号”，复用现有 Lisp tokenizer/parser。
    # 这样可以天然支持数字、字符串（保留引号）、嵌套调用 (peek 1 "ram") 等。
    wrapped_lines: List[str] = []
    for raw in source.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#!"):
            # 文件指令行：交给 runner 处理，这里跳过
            continue
        if line.startswith(";"):
            # 行注释
            continue
        # 支持 # 注释（Lisp tokenizer 已支持 ; 注释）
        if "#" in line:
            line = line.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("(") and line.endswith(")"):
            wrapped_lines.append(line)
        else:
            wrapped_lines.append(f"({line})")

    program = parse_lisp_tokens(tokenize("\n".join(wrapped_lines)))
    # 额外校验：行式语法要求每条 form 都是调用列表
    for form in program.forms:
        if not isinstance(form, list) or not form or not isinstance(form[0], Symbol):
            raise ValueError("line frontend: each line must start with a symbol name")
    return program

