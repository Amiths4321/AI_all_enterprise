import json
import os
from datetime import datetime


class RetrievalLogger:
    def __init__(self, path="logs/retrieval.jsonl"):
        self.path = path

        directory = os.path.dirname(path)

        if directory:
            os.makedirs(directory, exist_ok=True)

    def log(
        self,
        query,
        results,
        elapsed_seconds,
        mode="multivector",
        timings=None,
        metadata=None,
    ):
        record = {
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "query": query,
            "elapsed_seconds": round(
                elapsed_seconds,
                4,
            ),
            "results": results,
        }

        if timings:
            record["timings"] = {
                key: round(value, 4)
                for key, value in timings.items()
            }

        if metadata:
            record["metadata"] = metadata

        with open(
            self.path,
            "a",
            encoding="utf-8",
        ) as f:
            f.write(
                json.dumps(
                    record,
                    ensure_ascii=False,
                )
                + "\n"
            )