# Модуль с базовым классом репортов.
import importlib.util
import os
import sys

class ValidationError(Exception):
    pass


class BaseReport:
    """Базовый класс для создания репортов. Приводит ячейки таблиц к типам, заданным в схеме."""
    __name__ = 'base_report'
    __report_schema__ = None

    def __init__(self, table: list[tuple]) -> list[tuple]:
        if not self.__report_schema__:
            raise ValidationError(f'Необходимо задать схему данных для репорта в {self.__name__}!')
        self.table = self._read_by_report_schema(table)

    def _read_by_report_schema(self, table: list[tuple]) -> list[tuple]:
        """Прочитай табличку по схеме репорта, заданного внутри класса."""
        header_schema = tuple((name for name, _ in self.__report_schema__))
        body_schema = tuple((_type for _, _type in self.__report_schema__))

        head, body = table[0], table[1:]
        if head != header_schema:
            raise ValidationError(f'Получены заголовки репорта: "{head}", ожидаю: "{header_schema}"')

        normalized = []
        for record in body:
            normalized_record = (_type(value) for value, _type in zip(record, body_schema))
            normalized.append(tuple(normalized_record))
        return [head, *normalized]


def select_reporter_by_name(report_name: str):
    report_path = os.path.join("reports", f"{report_name}.py")

    if not os.path.isfile(report_path):
        print(f"Ошибка: {report_path} не найден")
        sys.exit(1)

    spec = importlib.util.spec_from_file_location(report_name, report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module.Report
