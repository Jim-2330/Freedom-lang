from __future__ import annotations

import sys
from pathlib import Path

# 包位于 python/freedon_lang，测试从仓库根目录运行时加入该路径
_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_ROOT / "python"))
