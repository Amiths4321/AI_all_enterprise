import json
import os
import platform
import subprocess
import sys
from datetime import datetime


def get_package_versions():
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        return []

    return [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def main():
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "python": {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
        },
        "environment": {
            "ollama_base_url": os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434",
            ),
            "embedding_model": os.getenv(
                "EMBEDDING_MODEL",
                "nomic-embed-text",
            ),
            "llm_model": os.getenv(
                "LLM_MODEL",
                "qwen2.5vl",
            ),
        },
        "packages": get_package_versions(),
    }

    output = "tests/system_snapshot.json"

    with open(
        output,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            snapshot,
            f,
            indent=2,
            ensure_ascii=False,
        )

    print("=" * 80)
    print("SYSTEM SNAPSHOT")
    print("=" * 80)

    print(
        f"\nPython: "
        f"{snapshot['python']['version']}"
    )

    print(
        f"Embedding: "
        f"{snapshot['environment']['embedding_model']}"
    )

    print(
        f"LLM: "
        f"{snapshot['environment']['llm_model']}"
    )

    print(
        f"\nSaved to: {output}"
    )


if __name__ == "__main__":
    main()