"""Базовые сущности для работы с репортами."""
from typing import List, Tuple, Type

from exceptions import ValidationError


class BaseReport:
    """Базовый класс для создания репортов.

    Парсит табличку, используя схему данных из `self.__report_schema__`,
    хранит результат парсинга в `self.table`.

    Классы-наследники могут прописать свою схему таблицы.
    Логика репортов добавляется через перезагрузку метода `self.calculate`.
    """
    __name__: str = "base_report"
    __report_schema__: List[Tuple[str, Type]] = None

    def __init__(self, table: List[tuple]):
        """Перед иницилизацией можно задать схему рабочей таблицы.

        Формат схемы - список кортежей, где первое значение - имя колонки, а
        второе - функция приведения типа, пример:

        `__report_schema__ = [('name': str), ('price', int), ...]`

        Если схема не задана, работаем с таблицей "как есть".
        """
        if self.__report_schema__:
            self.table = self._apply_schema(table)
        else:
            self.table = table

    def _apply_schema(self, table: List[tuple]) -> List[tuple]:
        """Приводит таблицу к типам, заданным в __report_schema__."""
        header_schema = tuple(name for name, _ in self.__report_schema__)
        type_schema = tuple(_type for _, _type in self.__report_schema__)

        head, *body = table
        if head != header_schema:
            raise ValidationError(
                "Заголовки репорта не совпадают. "
                f"Получено: {head}, ожидается: {header_schema}"
            )

        normalized_body = [
            tuple(_type(value) for value, _type in zip(record, type_schema))
            for record in body
        ]

        return [head, *normalized_body]

    def calculate(self) -> List[tuple]:
        """Функция, внутри которой задается бизнес-логика репорта.

        Репорт высчитывается на основании данных в `self.table`.
        Метод должен возвращать новую табличку с результатами репорта.
        """
        raise NotImplementedError(
            f"В {self.__name__} не определен метод calculate"
        )
