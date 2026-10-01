from statistics import mean


def average_latency(
    latencies: list[float],
) -> float:

    if not latencies:
        return 0.0

    return mean(latencies)


def percentile(
    values: list[float],
    percentile_value: float,
) -> float:

    if not values:
        return 0.0

    ordered = sorted(values)

    index = (
        percentile_value
        / 100
        * (len(ordered) - 1)
    )

    lower = int(index)
    upper = min(
        lower + 1,
        len(ordered) - 1,
    )

    fraction = index - lower

    return (
        ordered[lower]
        + (
            ordered[upper]
            - ordered[lower]
        )
        * fraction
    )