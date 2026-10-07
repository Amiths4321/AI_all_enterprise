import logging
import time


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def timed(name):

    def decorator(function):

        def wrapper(*args, **kwargs):

            start = time.perf_counter()

            try:
                return function(
                    *args,
                    **kwargs,
                )

            finally:
                elapsed = (
                    time.perf_counter()
                    - start
                )

                logging.info(
                    "%s took %.3f seconds",
                    name,
                    elapsed,
                )

        return wrapper

    return decorator