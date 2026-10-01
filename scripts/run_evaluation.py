import subprocess
import sys


def main():

    print("Running regression tests...")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            "tests",
            "-v",
        ]
    )

    if result.returncode != 0:
        print(
            "REGRESSION TESTS FAILED"
        )

        raise SystemExit(
            result.returncode
        )

    print(
        "REGRESSION TESTS PASSED"
    )


if __name__ == "__main__":
    main()