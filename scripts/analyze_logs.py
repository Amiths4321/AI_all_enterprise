import json
import os
import statistics


LOG_PATH = "logs/retrieval.jsonl"


def main():
    if not os.path.exists(LOG_PATH):
        print("No retrieval log found.")
        return

    records = []

    with open(
        LOG_PATH,
        "r",
        encoding="utf-8",
    ) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            try:
                records.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    if not records:
        print("No valid retrieval records found.")
        return

    print("=" * 90)
    print("RETRIEVAL LOG ANALYSIS")
    print("=" * 90)

    print(f"\nRecords: {len(records)}")

    modes = {}

    for record in records:
        mode = record.get(
            "mode",
            "unknown",
        )

        modes.setdefault(
            mode,
            [],
        ).append(record)

    for mode, items in modes.items():
        print("\n" + "-" * 90)
        print(f"MODE: {mode}")
        print("-" * 90)

        latencies = [
            item["elapsed_seconds"]
            for item in items
            if "elapsed_seconds" in item
        ]

        if latencies:
            print(
                f"Average latency: "
                f"{statistics.mean(latencies):.3f}s"
            )

            print(
                f"Min latency:     "
                f"{min(latencies):.3f}s"
            )

            print(
                f"Max latency:     "
                f"{max(latencies):.3f}s"
            )

        timing_names = [
            "retrieval",
            "aggregation",
            "rerank",
            "generation",
        ]

        for timing_name in timing_names:
            values = []

            for item in items:
                timings = item.get(
                    "timings",
                    {},
                )

                if timing_name in timings:
                    values.append(
                        timings[timing_name]
                    )

            if values:
                print(
                    f"Average {timing_name:<12}"
                    f"{statistics.mean(values):.3f}s"
                )

    print("\n" + "=" * 90)


if __name__ == "__main__":
    main()