#!/usr/bin/env python3
"""Run the repository test suite without requiring ambient PYTHONPATH."""

from pathlib import Path
import os
import sys
import unittest


ROOT = Path(__file__).resolve().parent
SOURCE = str(ROOT / "src")


def main() -> int:
    sys.path.insert(0, SOURCE)
    os.environ["PYTHONPATH"] = os.pathsep.join(
        part for part in (SOURCE, os.environ.get("PYTHONPATH")) if part
    )
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
