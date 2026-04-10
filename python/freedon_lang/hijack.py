from __future__ import annotations

from typing import Any, Callable, Dict


HijackWrapper = Callable[[Callable[..., Any], tuple, dict], Any]


class HijackRegistry:
    """维护被劫持的符号及其包装逻辑。"""

    def __init__(self) -> None:
        self._wrappers: Dict[str, HijackWrapper] = {}

    def register(self, name: str, wrapper: HijackWrapper) -> None:
        self._wrappers[name] = wrapper

    def remove(self, name: str) -> None:
        self._wrappers.pop(name, None)

    def wrap_call(self, name: str, fn: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        wrapper = self._wrappers.get(name)
        if wrapper is None:
            return fn(*args, **kwargs)
        return wrapper(fn, args, kwargs)


HIJACK_REGISTRY = HijackRegistry()

