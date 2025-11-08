from reports.base import BaseReport

class AverageRatingReport(BaseReport):
    __name__ = 'average_rating_report'
    __report_schema__ =  [
        ("name", str),
        ("brand", str),
        ("price", int),
        ("rating", float)
    ]

    def build(self) -> list[tuple]:
        brand_ratings: dict[str, list] = {}
        for name, brand, price, rating in self.table[1:]:
            try:
                brand_ratings[brand].append(rating)
            except KeyError:
                brand_ratings[brand] = [rating]

        # Считаем среднюю оценку для каждого бренда
        average_brand_rating: list[tuple] = []
        for brand, rating in brand_ratings.items():
            average_brand_rating += (brand, sum(rating))
        return average_brand_rating

Report = AverageRatingReport
__all__ = ['Report']