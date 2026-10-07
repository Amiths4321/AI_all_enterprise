from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_step(name: str, command: list[str]) -> bool:
    print(f"\n{'=' * 70}")
    print(name)
    print("=" * 70)

    result = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        print(f"\nFAILED: {name}")
        return False

    print(f"\nPASSED: {name}")
    return True


def main() -> int:
    steps = [
        (
            "Unit and integration tests",
            [sys.executable, "-m", "pytest", "tests", "-v"],
        ),
        (
            "Retrieval evaluation",
            [sys.executable, "scripts/evaluate_retrieval.py"],
        ),
    ]

    failures = 0

    for name, command in steps:
        if not run_step(name, command):
            failures += 1

    print(f"\n{'=' * 70}")
    print("FINAL VALIDATION")
    print("=" * 70)

    if failures:
        print(f"FAILED: {failures} validation step(s)")
        return 1

    print("PASSED: all validation steps")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())