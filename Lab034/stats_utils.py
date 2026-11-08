import statistics


def get_average(values: list[float]) -> float | None:
    """Повертає середнє значення списку."""
    return round(statistics.mean(values), 2) if values else None


def get_min(values: list[float]) -> float | None:
    """Повертає мінімальне значення."""
    return min(values) if values else None


def get_max(values: list[float]) -> float | None:
    """Повертає максимальне значення."""
    return max(values) if values else None


def get_median(values: list[float]) -> float | None:
    """Повертає медіану."""
    return round(statistics.median(values), 2) if values else None


def detect_jumps(
    values: list[float],
    timestamps: list[str],
    threshold: float
) -> list[str]:
    """Виявляє різкі перепади між сусідніми значеннями."""
    jumps = []

    for i in range(1, len(values)):
        if abs(values[i] - values[i - 1]) > threshold:
            jumps.append(timestamps[i])

    return jumps


def print_table(
    parameter_name: str,
    data_dict: dict[str, float]
) -> None:
    """Виводить таблицю з показниками певного параметра."""
    print(f"\nПоказники для параметра: {parameter_name}")
    print("+----------------------+-------------+")
    print(f"| {'Timestamp':<20} | {parameter_name:<11} |")
    print("+----------------------+-------------+")

    for timestamp, value in data_dict.items():
        print(f"| {timestamp:<20} | {value:<11} |")

    print("+----------------------+-------------+")


def print_results(
    parameter_name: str,
    results: dict
) -> None:
    """Виводить результати обчислень для параметра."""
    print(f"\nРезультати для параметра: {parameter_name}")

    for name, value in results.items():
        print(f"{name}: {value}")