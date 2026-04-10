from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class PersistentStore:
    data: Dict[str, Any] = field(default_factory=dict)
    path: Optional[Path] = None

    def get(self, key: Any, default: Any = None) -> Any:
        return self.data.get(str(key), default)

    def set(self, key: Any, value: Any) -> Any:
        self.data[str(key)] = value
        return value

    def load(self, path: str | Path) -> None:
        p = Path(path)
        if p.exists():
            self.data = json.loads(p.read_text(encoding="utf-8"))
        else:
            self.data = {}
        self.path = p

    def save(self, path: str | Path | None = None) -> None:
        p = Path(path) if path is not None else self.path
        if p is None:
            raise ValueError("store-save: no path provided and no previous store-load path")
        p.write_text(json.dumps(self.data, ensure_ascii=False, indent=2), encoding="utf-8")
        self.path = p


GLOBAL_STORE = PersistentStore()

