from __future__ import annotations

import argparse
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT / "python"))

from freedon_lang import run_file, run_repl


def main() -> None:
    parser = argparse.ArgumentParser(description="Freedon Lang v0.1-Alpha")
    parser.add_argument("file", nargs="?", help="Freedon 源文件 (.fd)")
    args = parser.parse_args()

    if args.file:
        path = Path(args.file)
        run_file(path)
    else:
        run_repl()


if __name__ == "__main__":
    main()

