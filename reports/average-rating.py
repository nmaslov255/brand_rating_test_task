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
        average_brand_rating: list[tuple] = [('', 'brand', 'rating')]
        for idx, brand_statistic in enumerate(brand_ratings.items()):
            brand, votes = brand_statistic
            rating = sum(votes) / len(votes)
            average_brand_rating.append((idx+1, brand, rating,))
        return average_brand_rating

Report = AverageRatingReport
__all__ = ['Report']