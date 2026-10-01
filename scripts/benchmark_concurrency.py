from concurrent.futures import (
    ThreadPoolExecutor,
)
from time import perf_counter


QUESTIONS = [
    "How many annual leave days do employees receive?",
    "How do employees submit annual leave requests?",
    "What is required for production deployments?",
    "Who reviews the annual operating budget?",
]


def run_query(question):

    # Replace with your actual service call.
    return question


def run_sequential():

    started = perf_counter()

    for question in QUESTIONS:
        run_query(question)

    return (
        perf_counter() - started
    ) * 1000


def run_concurrent():

    started = perf_counter()

    with ThreadPoolExecutor(
        max_workers=4
    ) as executor:

        list(
            executor.map(
                run_query,
                QUESTIONS,
            )
        )

    return (
        perf_counter() - started
    ) * 1000


def main():

    sequential = run_sequential()
    concurrent = run_concurrent()

    print(
        f"Sequential: "
        f"{sequential:.2f} ms"
    )

    print(
        f"Concurrent: "
        f"{concurrent:.2f} ms"
    )


if __name__ == "__main__":
    main()