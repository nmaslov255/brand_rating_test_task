# Модуль с базовым классом репортов.

class ValidationError(Exception):
    pass


class BaseReport:
    """Базовый класс для создания репортов. Приводит ячейки таблиц к типам, заданным в схеме."""
    __table_schema__ = None

    def __init__(self, table: list[tuple]) -> list[tuple]:
        self.table = self._pre_processor(table)

    def _pre_processor(self, table: list[tuple]) -> list[tuple]:
        if not self.__table_schema__:
            return table

        header_schema = tuple((name for name, _ in self.__table_schema__))
        body_schema = tuple((_type for _, _type in self.__table_schema__))

        head, body = (table[0], table[1:])
        if head != header_schema:
            raise ValidationError(f'Невалидный заголовок {head}, ожидается {header_schema}')

        normalized = []
        for record in body:
            normalized_record = (_type(value) for value, _type in zip(record, body_schema))
            normalized.append(tuple(normalized_record))
        return [head, *normalized]
