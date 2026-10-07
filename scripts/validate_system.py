import os
import sys


REQUIRED_FILES = [
    "src/retrieval/parent_child.py",
    "src/retrieval/reranker.py",
    "src/retrieval/multivector/store.py",
    "src/retrieval/multivector/generator_v2.py",
    "src/retrieval/multivector/query_expander.py",
    "src/rag/pipeline.py",
    "src/rag/multivector_pipeline.py",
    "src/rag/query_rewriter.py",
    "src/rag/unified_pipeline.py",
    "src/rag/memory.py",
    "src/rag/retrieval_logger.py",
    "api/main.py",
    "scripts/check_multivector.py",
    "scripts/validate_multivector.py",
    "scripts/benchmark_retrievers.py",
    "scripts/run_full_benchmark.py",
]


def check_files():
    missing = [
        path
        for path in REQUIRED_FILES
        if not os.path.exists(path)
    ]

    print("=" * 80)
    print("ENTERPRISE RAG SYSTEM VALIDATION")
    print("=" * 80)

    print("\nRequired files:")

    if missing:
        print(f"\nMISSING: {len(missing)}")

        for path in missing:
            print(f"  [FAIL] {path}")

        return False

    print(
        f"  [PASS] "
        f"{len(REQUIRED_FILES)} files present"
    )

    return True


def check_directories():
    directories = [
        "src",
        "src/rag",
        "src/retrieval",
        "src/retrieval/multivector",
        "scripts",
        "tests",
        "logs",
        "chroma_db",
        "multivector_db",
    ]

    missing = [
        path
        for path in directories
        if not os.path.isdir(path)
    ]

    print("\nRequired directories:")

    if missing:
        for path in missing:
            print(f"  [FAIL] {path}")

        return False

    print(
        f"  [PASS] "
        f"{len(directories)} directories present"
    )

    return True


def check_data():
    files = [
        "parent_store.json",
        "tests/multivector_questions.json",
        "tests/answer_questions.json",
    ]

    missing = [
        path
        for path in files
        if not os.path.exists(path)
    ]

    print("\nRequired data/config files:")

    if missing:
        for path in missing:
            print(f"  [FAIL] {path}")

        return False

    print(
        f"  [PASS] "
        f"{len(files)} files present"
    )

    return True


def main():
    checks = [
        check_files(),
        check_directories(),
        check_data(),
    ]

    print("\n" + "=" * 80)

    if all(checks):
        print("SYSTEM VALIDATION: PASS")
        print("=" * 80)
        return

    print("SYSTEM VALIDATION: FAIL")
    print("=" * 80)

    sys.exit(1)


if __name__ == "__main__":
    main()