from dataclasses import dataclass
from time import monotonic
from typing import Any


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:

    def __init__(
        self,
        ttl_seconds: float = 60,
        max_size: int = 1000,
    ):
        self.ttl_seconds = ttl_seconds
        self.max_size = max_size
        self._data: dict[str, CacheEntry] = {}

    def get(self, key: str):

        entry = self._data.get(key)

        if entry is None:
            return None

        if monotonic() >= entry.expires_at:
            del self._data[key]
            return None

        return entry.value

    def set(
        self,
        key: str,
        value,
    ):

        if len(self._data) >= self.max_size:
            oldest_key = next(
                iter(self._data)
            )

            del self._data[oldest_key]

        self._data[key] = CacheEntry(
            value=value,
            expires_at=(
                monotonic()
                + self.ttl_seconds
            ),
        )

    def clear(self):
        self._data.clear()

    def __len__(self):
        return len(self._data)