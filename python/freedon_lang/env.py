from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class Env:
    data: Dict[str, Any] = field(default_factory=dict)
    parent: Optional["Env"] = None

    def find(self, name: str) -> "Env | None":
        if name in self.data:
            return self
        if self.parent is not None:
            return self.parent.find(name)
        return None

    def get(self, name: str) -> Any:
        env = self.find(name)
        if env is None:
            raise NameError(f"Unbound symbol: {name}")
        return env.data[name]

    def set(self, name: str, value: Any) -> None:
        self.data[name] = value

