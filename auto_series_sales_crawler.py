import csv
import time
import random

import requests

from constants import UTF_SIG, HEADERS, RankDataType, OUTTER_DETAIL_TYPES
from series_sales import SeriesSales


class AutoSalesCrawler:
    # local csv header for automotive sales data
    LOCAL_CSV_HEADER = ['city', 'series_id', 'series_name', 'brand_id', 'brand_name', 'sub_brand_id', 'sub_brand_name',
                        'min_price', 'max_price', 'dealer_price', 'outter_detail_type', 'count', 'rank', 'last_rank']

    # 懂车帝城市列表
    CITIES_URL = 'https://www.dongchedi.com/motor/dealer/m/v1/get_dealer_city_list/'

    # 懂车帝销量数据
    SALES_URL = ('https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name={}&count={}'
                 '&offset={}&month=&new_energy_type=&rank_data_type={}'
                 '&brand_id=&price=&manufacturer=&outter_detail_type=&nation=0')

    def __init__(self):
        self.cities = []
        self.nation_sales_data = [SeriesSales]
        self.cities_sales_data = [SeriesSales]
        self.auto_sales_data = {}

    def load_sales_data(self, from_csv=False, nation_csv_file='auto_sales_data_nation.csv',
                        cities_csv_file='auto_sales_data_cities.csv'):
        if from_csv:
            self.load_sales_data_from_csv(nation_csv_file, cities_csv_file)
        else:
            self.crawl_nation_sales_data(nation_csv_file)
            self.crawl_cities_sales_data(cities_csv_file)

    def load_sales_data_from_csv(self, nation_csv_file, cities_csv_file):
        self.nation_sales_data = []
        with open(nation_csv_file, 'r', encoding=UTF_SIG) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.nation_sales_data.append(SeriesSales.from_dict(row))
        print('全国销量数据', len(self.nation_sales_data))

        self.cities_sales_data = []
        with open(cities_csv_file, 'r', encoding=UTF_SIG) as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.cities_sales_data.append(SeriesSales.from_dict(row))
        print('城市销量数据', len(self.cities_sales_data))

    def crawl_nation_sales_data(self, nation_csv_file):
        self.nation_sales_data = self.get_sales_data(city='全国')
        print('全国销量数据', len(self.nation_sales_data))
        self.save_to_local_csv(self.nation_sales_data, nation_csv_file)

    def crawl_cities_sales_data(self, cities_csv_file):
        # 获取城市列表
        self.get_cities()
        # 按城市获取销量数据
        self.cities_sales_data = []
        # count = 0
        for city in self.cities:
            time.sleep(random.randint(1, 3))
            city_data = self.get_sales_data(city)
            # 打印销量数据数量
            print(city, len(city_data))
            if len(city_data) > 0:
                self.cities_sales_data.extend(city_data)
            # count += 1
            # if count > 5:
            #     break
        print('城市销量数据', len(self.cities_sales_data))
        self.save_to_local_csv(self.cities_sales_data, cities_csv_file)

    def save_to_local_csv(self, sales_data, csv_file):
        with open(csv_file, 'w', newline='', encoding=UTF_SIG) as f:
            writer = csv.DictWriter(f, self.LOCAL_CSV_HEADER)
            writer.writeheader()
            writer.writerows([sales.toDict() for sales in sales_data])

    # 获取销量数据
    def get_sales_data(self, city='全国'):
        page_size = 500
        offset = 0
        data_count = 500
        # 逐页获取销量数据
        total_sales_list = []
        while data_count == page_size:
            if city == '全国':
                rank_data_type = RankDataType.NATION.value
            else:
                rank_data_type = RankDataType.CITY.value
            url = self.SALES_URL.format(requests.utils.quote(city), page_size, offset, rank_data_type)
            response = requests.get(url)
            json_data = response.json()
            data_count = len(json_data['data']['list']) if json_data['data']['list'] else 0
            if data_count > 0:
                sales_data = self.parse_sales_data(json_data, city)
                total_sales_list.extend(sales_data)
            offset += page_size
        return total_sales_list

    # 从json中提取数据
    def parse_sales_data(self, json_data, city_name):
        sales_data = []
        for item in json_data['data']['list']:
            sales_data.append(SeriesSales.from_json(item, city_name))
        return sales_data

    # 获取所有的城市列表
    def get_cities(self):
        response = requests.get(self.CITIES_URL, headers=HEADERS)
        json_data = response.json()
        self.cities = []
        for item in json_data['data']:
            for city in item['city']:
                self.cities.append(city['city_name'])

    # 导出销量数据到csv中
    def export_sales_data_to_csv(self, csv_file='auto_sales_data.csv'):
        # 将车型在每个城市的销量数据存储在一个dict中，key为series_id，value为一个dict，key为city_name，value为count
        # 例如：{1: {'北京': 100, '上海': 200}}
        series_city_sales_data = {}
        for item in self.cities_sales_data:
            series_id = item.series_id
            city = item.city
            count = item.city_sales
            if series_id not in series_city_sales_data:
                series_city_sales_data[series_id] = {}
            series_city_sales_data[series_id][city] = count

        # 从cities_sales_data中获取城市列表，存储在set中
        # 在生成csv时，只保留有销量的城市
        cities_set = set()
        for item in self.cities_sales_data:
            cities_set.add(item.city)
        print('cities count:', len(cities_set))

        # 整理导出数据，每个车型一行，包括全国销量和各城市销量
        exported_sales_data = []
        for series_nation_sales_data in self.nation_sales_data:
            row = {}
            series_id = series_nation_sales_data.series_id
            row['series_name'] = series_nation_sales_data.series_name
            row['brand_name'] = series_nation_sales_data.brand_name
            row['sub_brand_name'] = series_nation_sales_data.sub_brand_name

            row['min_price'] = series_nation_sales_data.min_price
            row['max_price'] = series_nation_sales_data.max_price
            row['dealer_price'] = series_nation_sales_data.dealer_price
            outter_detail_type = int(series_nation_sales_data.outter_detail_type)
            row['outter_detail_type'] = OUTTER_DETAIL_TYPES[
                outter_detail_type] if outter_detail_type in OUTTER_DETAIL_TYPES else 'N/A'
            row['rank'] = series_nation_sales_data.rank
            row['last_rank'] = series_nation_sales_data.last_rank
            row['全国'] = series_nation_sales_data.city_sales
            if series_id in series_city_sales_data:
                city_sales_data = series_city_sales_data[series_id]
                for city in cities_set:
                    if city in city_sales_data:
                        row[city] = city_sales_data[city]
                    else:
                        row[city] = 0
            exported_sales_data.append(row)
        # 写入csv文件
        exported_csv_header = ['series_name', 'brand_name', 'sub_brand_name', 'min_price', 'max_price', 'dealer_price',
                               'outter_detail_type', 'rank', 'last_rank', "全国"]
        for city in cities_set:
            exported_csv_header.append(city)
        with open(csv_file, 'w', newline='', encoding=UTF_SIG) as f:
            writer = csv.DictWriter(f, exported_csv_header)
            writer.writeheader()
            writer.writerows(exported_sales_data)
