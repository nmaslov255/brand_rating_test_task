#!/usr/bin/env python3
import argparse
import importlib.util
import os
import sys
import csv

from tabulate import tabulate


def build_report_by_name(report_name: str):
    report_path = os.path.join("reports", f"{report_name}.py")

    if not os.path.isfile(report_path):
        print(f"Ошибка: {report_path} не найден")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location(report_name, report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.Report


def merge_csv(file_paths: list) -> list[tuple]:
    """
    Объединяет список из нескольких csv файлов

    :param file_paths: list[str] — пути к CSV файлам
    :return: list[tuple] — Объединенный список из csv файлов
    """

    head = None
    normalized = []

    for file_path in file_paths:
        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            
            if not head:  # Создаем заголовок csv файла
                head = next(reader)
                normalized.append(tuple(head))
            elif head != next(reader):  # Возбуждаем исключение, если csv заголовок нового файла отличается по структуре
                raise Exception(f'Структура заголовка {file_path} отличается от других переданных файлов!')

            for record in reader:
                normalized.append(tuple(record))
    return normalized

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

    records = merge_csv(args.files)
    Reporter = build_report_by_name(args.report)(records)

    report = Reporter.build()
    print(tabulate(report, headers="firstrow"))


if __name__ == "__main__":
    main()
