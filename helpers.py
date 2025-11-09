# Функции-помошники для работы с файлами
import csv


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