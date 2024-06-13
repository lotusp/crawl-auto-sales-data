class SeriesSales:
    def __init__(self, series_id, series_name, brand_id, brand_name, sub_brand_id, sub_brand_name, min_price, max_price,
                 dealer_price, outter_detail_type, rank, last_rank, city, city_sales):
        self.series_id = series_id
        self.series_name = series_name
        self.brand_id = brand_id
        self.brand_name = brand_name
        self.sub_brand_id = sub_brand_id
        self.sub_brand_name = sub_brand_name
        self.min_price = min_price
        self.max_price = max_price
        self.dealer_price = dealer_price
        self.outter_detail_type = outter_detail_type
        self.rank = rank
        self.last_rank = last_rank
        self.city = city
        self.city_sales = city_sales

    @classmethod
    def from_json(cls, item, city_name):
        return cls(
            item['series_id'],
            item['series_name'],
            item['brand_id'],
            item['brand_name'],
            item['sub_brand_id'],
            item['sub_brand_name'],
            item['min_price'],
            item['max_price'],
            item['dealer_price'],
            item['outter_detail_type'],
            item['rank'],
            item['last_rank'],
            city_name,
            item['count']
        )

    def toDict(self):
        return {
            'series_id': self.series_id,
            'series_name': self.series_name,
            'brand_id': self.brand_id,
            'brand_name': self.brand_name,
            'sub_brand_id': self.sub_brand_id,
            'sub_brand_name': self.sub_brand_name,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'dealer_price': self.dealer_price,
            'outter_detail_type': self.outter_detail_type,
            'rank': self.rank,
            'last_rank': self.last_rank,
            'city': self.city,
            'count': self.city_sales
        }

    @classmethod
    def from_dict(cls, dict):
        return cls(
            dict['series_id'],
            dict['series_name'],
            dict['brand_id'],
            dict['brand_name'],
            dict['sub_brand_id'],
            dict['sub_brand_name'],
            dict['min_price'],
            dict['max_price'],
            dict['dealer_price'],
            dict['outter_detail_type'],
            dict['rank'],
            dict['last_rank'],
            dict['city'],
            dict['count']
        )