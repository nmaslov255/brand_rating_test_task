#!/usr/bin/env python3
import argparse
from tabulate import tabulate

from helpers import merge_csv
from reports import select_reporter_by_name


def main():
    parser = argparse.ArgumentParser(
        description="CLI для генерации таблички в терминале."
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Список путей к CSV-файлам"
    )
    parser.add_argument(
        "--report",
        required=True,
        help="Название отчёта (имя модуля в директории reports, без расширения .py)"
    )

    args = parser.parse_args()
    Reporter = select_reporter_by_name(args.report)

    table = merge_csv(args.files)
    report = Reporter(table).build()

    print(tabulate(report, headers="firstrow"))


if __name__ == "__main__":
    main()
