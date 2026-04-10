from __future__ import annotations

from typing import Any, Dict, Tuple


class VirtualGlobalMemory:
    """虚拟「全域寻址」内存表。

    在 Alpha 原型中，我们不直接访问真实物理内存，而是通过一张全局表
    来模拟任意地址的读写行为。
    """

    def __init__(self) -> None:
        # key: (space, address) -> Any
        # address 可以是 int（内存/显存）或 str（寄存器名）等
        self._mem: Dict[Tuple[str, object], Any] = {}

    def peek(self, addr: Any, space: str = "default") -> Any:
        key = (space, self._normalize_addr(addr))
        return self._mem.get(key)

    def poke(self, addr: Any, value: Any, space: str = "default") -> Any:
        key = (space, self._normalize_addr(addr))
        self._mem[key] = value
        return value

    def _normalize_addr(self, addr: Any) -> object:
        if isinstance(addr, bool):
            return int(addr)
        if isinstance(addr, int):
            return addr
        if isinstance(addr, float) and addr.is_integer():
            return int(addr)
        if isinstance(addr, str):
            return addr
        return str(addr)


GLOBAL_MEMORY = VirtualGlobalMemory()

