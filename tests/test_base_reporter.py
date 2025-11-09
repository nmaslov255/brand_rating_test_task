import pytest

from reports.base import BaseReport, ValidationError


class DummyReport(BaseReport):
    __report_schema__ = [
        ("name", str),
        ("price", int),
        ("rating", float)
    ]


def test_base_report_applies_schema():
    table = [
        ("name", "price", "rating"),
        ("A", "100", "4.5"),
        ("B", "200", "3.8"),
    ]
    report = DummyReport(table)
    # Проверяем, что типы применены
    assert report.table[1] == ("A", 100, 4.5)
    assert report.table[2] == ("B", 200, 3.8)


def test_base_report_invalid_header():
    table = [
        ("wrong", "header", "cols"),
        ("A", "100", "4.5"),
    ]
    with pytest.raises(ValidationError):
        DummyReport(table)


def test_base_report_missing_schema():
    class NoSchemaReport(BaseReport):
        pass

    table = [("a", "b"), ("1", "2")]
    with pytest.raises(ValidationError):
        NoSchemaReport(table)