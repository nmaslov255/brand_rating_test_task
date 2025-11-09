import os
import csv
import pytest
from io import StringIO
from tempfile import NamedTemporaryFile

from helpers import merge_csv
from reports.base import ValidationError


def create_temp_csv(content: str):
    """Создаёт временный CSV файл и возвращает его путь"""
    tmp = NamedTemporaryFile(mode='w+', newline='', delete=False)
    tmp.write(content)
    tmp.flush()
    tmp.close()
    return tmp.name


def test_merge_csv_single_file():
    content = "name,brand,price,rating\nA,BrandA,100,4.5\nB,BrandB,200,3.8\n"
    path = create_temp_csv(content)
    
    merged = merge_csv([path])
    assert merged == [
        ("name", "brand", "price", "rating"),
        ("A", "BrandA", "100", "4.5"),
        ("B", "BrandB", "200", "3.8"),
    ]
    
    os.remove(path)


def test_merge_csv_multiple_files_same_header():
    content1 = "name,brand,price,rating\nA,BrandA,100,4.5\n"
    content2 = "name,brand,price,rating\nB,BrandB,200,3.8\n"
    path1 = create_temp_csv(content1)
    path2 = create_temp_csv(content2)

    merged = merge_csv([path1, path2])
    assert merged == [
        ("name", "brand", "price", "rating"),
        ("A", "BrandA", "100", "4.5"),
        ("B", "BrandB", "200", "3.8"),
    ]

    os.remove(path1)
    os.remove(path2)


def test_merge_csv_different_headers_raises():
    content1 = "name,brand,price,rating\nA,BrandA,100,4.5\n"
    content2 = "name,brand,cost,rating\nB,BrandB,200,3.8\n"
    path1 = create_temp_csv(content1)
    path2 = create_temp_csv(content2)

    with pytest.raises(ValidationError):
        merge_csv([path1, path2])

    os.remove(path1)
    os.remove(path2)
