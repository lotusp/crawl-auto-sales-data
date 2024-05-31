class SeriesScores:
    def __init__(self, series_id, brand_id, brand_name, sub_brand_id, sub_brand_name, series_name, scores, ranks):
        self.series_id = series_id
        self.brand_id = brand_id
        self.brand_name = brand_name
        self.sub_brand_id = sub_brand_id
        self.sub_brand_name = sub_brand_name
        self.series_name = series_name
        self.scores = scores
        self.ranks = ranks

    @classmethod
    def from_json(cls, score_type, item):
        scores = {score_type: float(item['score']) / 100}
        ranks = {score_type: item['rank']}
        return cls(
            item['series_id'],
            item['brand_id'],
            item['brand_name'],
            item['sub_brand_id'],
            item['sub_brand_name'],
            item['series_name'],
            scores,
            ranks
        )

    def update_score_rank(self, score_type, item):
        self.scores[score_type] = float(item['score']) / 100
        self.ranks[score_type] = item['rank']
