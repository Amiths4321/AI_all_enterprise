import hashlib
import json
import os


class ResponseCache:

    def __init__(
        self,
        path="rag_cache.json",
    ):
        self.path = path

        if os.path.exists(path):
            with open(
                path,
                "r",
                encoding="utf-8",
            ) as f:
                self.cache = json.load(f)
        else:
            self.cache = {}

    def _key(self, query):

        return hashlib.sha256(
            query.strip()
            .lower()
            .encode("utf-8")
        ).hexdigest()

    def get(self, query):

        return self.cache.get(
            self._key(query)
        )

    def set(self, query, response):

        self.cache[
            self._key(query)
        ] = response

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                self.cache,
                f,
                ensure_ascii=False,
                indent=2,
            )