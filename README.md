# Тестовое задание: `Brand Rating Report CLI`

Этот проект генерирует отчеты по товарам на основе данных из CSV файлов.  
Сейчас поддерживается только обработка CSV таблиц с заголовками.  
Отчеты формируются путем выбора конкретного репорта из директории `reports/`.

---

## Установка и запуск

### 1. Создать и активировать виртуальное окружение

```bash
python3 -m venv env
source env/bin/activate
```

### 2. Установить зависимости
```bash
pip install -r requirements.txt
```

### 3. Запуск программы
```Bash
python main.py --files example/products1.csv example/products2.csv --report average-rating
```

Где:
--files принимает список путей к CSV файлам
--report указывает модуль репорта в директории reports/

#### Пример входных CSV файлов
Файлы c примерами лежат в example/products1.csv и example/products2.csv

```csv
name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
iphone 14,apple,799,4.7
galaxy a54,samsung,349,4.2
```

### Правила создания нового репорта
1. Создать новый файл в директории reports/, например:
```Bash
reports/my_new_report.py
```

2. Импортировать BaseReport:
```Python
from reports.base import BaseReport
```

3. Определить имя репорта и схему таблицы в свойстве `__report_schema__`:
```Python
class MyNewReport(BaseReport):
    __name__ = 'my_new_report'
    __report_schema__ = [
        ("brand", str),
        ("rating", float),
    ]
```

4. Перегрузить метод `self.calculate`:
```Python
class MyNewReport(BaseReport):
    ...  # Имя репорта и схема таблицы
    def calculate(self) -> list[tuple]:
        top_brand, top_rating = None, None
        for brand, rating in self.table[1:]:
            if not top_brand:
                top_brand, top_rating = record
            elif rating > top_rating:
                top_brand, top_rating = record
        return [('top_brand', 'top_rating'), (top_brand, top_rating)]
```

5. Определить публичный класс Report в конце файла:
```Python
Report = MyNewReport

__all__ = ["Report"]
```

Теперь репорт можно запускать:
```Bash
python main.py --files example/products1.csv example/products2.csv --report my-new-report
```

## Тестирование
В качестве стандарта кодирования используется pep8. Запуск автотестов и линтера:
```Bash
pytest && flake8
```

