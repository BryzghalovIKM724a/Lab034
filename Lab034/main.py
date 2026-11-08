import csv
import json
import configparser
import stats_utils as su


# Пороги різких перепадів
THRESHOLDS = {
    "temperature": 7,
    "humidity": 20,
    "pressure": 5000
}


def read_csv(filename: str) -> dict[str, dict[str, float]]:
    """Зчитує дані з CSV і повертає словник з показниками."""
    data = {
        "temperature": {},
        "humidity": {},
        "pressure": {}
    }

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            timestamp = row["timestamp"]

            data["temperature"][timestamp] = float(row["temperature"])
            data["humidity"][timestamp] = float(row["humidity"])
            data["pressure"][timestamp] = float(row["pressure"])

    return data


def read_config(filename: str) -> dict[str, list[str]]:
    """Зчитує файл конфігурації INI."""
    config = configparser.ConfigParser()
    config.read(filename, encoding="utf-8")

    settings = {}

    for section in config.sections():
        stats = config.get(section, "stats")
        settings[section] = [
            item.strip()
            for item in stats.split(",")
        ]

    return settings


def calculate_stats(
    parameter: str,
    data_dict: dict[str, float],
    stats_list: list[str]
) -> dict:
    """Обчислює характеристики відповідно до налаштувань."""
    values = list(data_dict.values())
    timestamps = list(data_dict.keys())

    result = {}

    if "average" in stats_list:
        result["average"] = su.get_average(values)

    if "min" in stats_list:
        result["min"] = su.get_min(values)

    if "max" in stats_list:
        result["max"] = su.get_max(values)

    if "median" in stats_list:
        result["median"] = su.get_median(values)

    if "jumps" in stats_list:
        result["jumps"] = su.detect_jumps(
            values,
            timestamps,
            THRESHOLDS[parameter]
        )

    return result


def main() -> None:
    try:
        # 1. Зчитування даних
        data = read_csv("data.csv")

        # 2. Зчитування налаштувань
        settings = read_config("config.ini")

        results = {}

        # 3. Обробка кожного параметра
        for parameter, stats_list in settings.items():

            if parameter not in data:
                continue

            su.print_table(
                parameter,
                data[parameter]
            )

            results[parameter] = calculate_stats(
                parameter,
                data[parameter],
                stats_list
            )

            su.print_results(
                parameter,
                results[parameter]
            )

        # 4. Збереження результатів у JSON
        with open(
            "results.json",
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                results,
                file,
                ensure_ascii=False,
                indent=4
            )

        print(
            "\nРезультати збережено у файлі results.json"
        )

    except FileNotFoundError as error:
        print(
            f"Помилка: файл не знайдено - {error.filename}"
        )

    except (ValueError, KeyError) as error:
        print(
            f"Помилка у форматі даних: {error}"
        )


if __name__ == "__main__":
    main()