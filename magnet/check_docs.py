"""Standalone check_docs entry for repro commands."""
from __future__ import annotations

import sys

from magnet.probes import check_docs_exit_code


def main() -> None:
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    raise SystemExit(check_docs_exit_code(root))


if __name__ == "__main__":
    main()
