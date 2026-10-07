import json
import logging
import sys

from app.core.request_context import (
    get_request_id,
)


class JsonFormatter(
    logging.Formatter
):

    def format(self, record):

        payload = {
            "timestamp": self.formatTime(
                record,
                "%Y-%m-%dT%H:%M:%S",
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": get_request_id(),
        }

        return json.dumps(payload)


def configure_logging():

    handler = logging.StreamHandler(
        sys.stdout
    )

    handler.setFormatter(
        JsonFormatter()
    )

    root = logging.getLogger()

    root.handlers.clear()
    root.addHandler(handler)

    root.setLevel(logging.INFO)