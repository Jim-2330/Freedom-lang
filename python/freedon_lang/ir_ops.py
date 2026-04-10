from __future__ import annotations

# IR1: (op_name, *operands) — 人类可读
# IR2: (opcode_int, *operands) — 与 IR1 同语义，仅操作码数值化

OP_PUSH = 0
OP_LOAD = 1
OP_APPLY = 2
OP_JUMP_IF_FALSE = 3
OP_JUMP = 4
OP_DEF = 5
OP_POP = 6
OP_MAKE_LAMBDA = 7

OP_NAMES: dict[str, int] = {
    "push": OP_PUSH,
    "load": OP_LOAD,
    "apply": OP_APPLY,
    "jump-if-false": OP_JUMP_IF_FALSE,
    "jump": OP_JUMP,
    "def": OP_DEF,
    "pop": OP_POP,
    "make-lambda": OP_MAKE_LAMBDA,
}

NAME_BY_OP: dict[int, str] = {v: k for k, v in OP_NAMES.items()}


def ir1_to_ir2(code: list[tuple]) -> list[tuple]:
    out: list[tuple] = []
    for inst in code:
        if not inst:
            continue
        name, *rest = inst
        if isinstance(name, int):
            out.append(tuple(inst))
            continue
        op = OP_NAMES[str(name)]
        if str(name) == "make-lambda":
            params, inner = rest
            inner2 = ir1_to_ir2(list(inner))
            out.append((op, params, tuple(inner2)))
        else:
            out.append((op, *rest))
    return out
