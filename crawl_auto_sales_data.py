import requests
import csv
import time
import random
import argparse

#  0-微型车，1-小型车，2-紧凑型车，3-中型车，4-中大型车，5-大型车
#  10-小型SUV，11-紧凑型SUV，12-中型SUV，13-中大型SUV，14-大型SUV
#  20-小型MPV，21-紧凑型MPV，22-中型MPV，23-中大型MPV，24-大型MPV
outter_detail_types = {
    0: '微型车',
    1: '小型车',
    2: '紧凑型车',
    3: '中型车',
    4: '中大型车',
    5: '大型车',
    10: '小型SUV',
    11: '紧凑型SUV',
    12: '中型SUV',
    13: '中大型SUV',
    14: '大型SUV',
    20: '小型MPV',
    21: '紧凑型MPV',
    22: '中型MPV',
    23: '中大型MPV',
    24: '大型MPV'
}

# 1-纯电动，2-插电式混动，3-增程式
new_energy_types = {
    0: 'N/A',
    1: '纯电动',
    2: '插电式混动',
    3: '增程式'
}

# request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

# local csv header for automotive sales data
local_csv_header = ['city', 'series_id', 'series_name', 'brand_id', 'brand_name', 'sub_brand_id', 'sub_brand_name',
                    'min_price', 'max_price', 'dealer_price', 'outter_detail_type', 'count', 'rank', 'last_rank']


# 获取销量数据
def get_sales_data(city='全国'):
    page_size = 500
    offset = 0
    data_count = 500
    # 逐页获取销量数据
    total_sales_list = []
    while data_count == page_size:
        if city == '全国':
            rank_data_type = 11
        else:
            rank_data_type = 64
        url = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name={}&count={}&offset={}&month=&new_energy_type=&rank_data_type={}&brand_id=&price=&manufacturer=&outter_detail_type=&nation=0'.format(
            requests.utils.quote(city), page_size, offset, rank_data_type)
        response = requests.get(url)
        json_data = response.json()
        data_count = len(json_data['data']['list']) if json_data['data']['list'] else 0
        if data_count > 0:
            sales_data = parse_sales_data(json_data, city)
            total_sales_list.extend(sales_data)
        offset += page_size
    return total_sales_list


# 从json中提取数据
def parse_sales_data(json_data, city_name):
    sales_data = []
    for item in json_data['data']['list']:
        sales_data.append({
            'city': city_name,
            'series_id': item['series_id'],
            'brand_id': item['brand_id'],
            'brand_name': item['brand_name'],
            'sub_brand_id': item['sub_brand_id'],
            'sub_brand_name': item['sub_brand_name'],
            'series_name': item['series_name'],
            'min_price': item['min_price'],
            'max_price': item['max_price'],
            'dealer_price': item['dealer_price'],
            'outter_detail_type': item['outter_detail_type'],
            # 'new_energy_type': item['new_energy_type'] if 'new_energy_type' in item else 0,
            'count': item['count'],
            'rank': item['rank'],
            'last_rank': item['last_rank']
        })
    return sales_data


# 获取所有的城市列表
def get_cities():
    url = 'https://www.dongchedi.com/motor/dealer/m/v1/get_dealer_city_list/'
    response = requests.get(url, headers=headers)
    json_data = response.json()
    cities = []
    for item in json_data['data']:
        for city in item['city']:
            cities.append(city['city_name'])
    return cities


# 导出销量数据到csv中
def export_sales_data_to_csv(nation_sales_data, cities_sales_data, csv_file='auto_sales_data.csv'):
    # 将车型在每个城市的销量数据存储在一个dict中，key为series_id，value为一个dict，key为city_name，value为count
    # 例如：{1: {'北京': 100, '上海': 200}}
    series_city_sales_data = {}
    for item in cities_sales_data:
        series_id = int(item['series_id'])
        city = item['city']
        count = item['count']
        if series_id not in series_city_sales_data:
            series_city_sales_data[series_id] = {}
        series_city_sales_data[series_id][city] = count

    # 从cities_sales_data中获取城市列表，存储在set中
    # 在生成csv时，只保留有销量的城市
    cities_set = set()
    for item in cities_sales_data:
        cities_set.add(item['city'])

    # 整理导出数据，每个车型一行，包括全国销量和各城市销量
    exported_sales_data = []
    for series_nation_sales_data in nation_sales_data:
        row = {}
        series_id = int(series_nation_sales_data['series_id'])
        row['series_name'] = series_nation_sales_data['series_name']
        row['brand_name'] = series_nation_sales_data['brand_name']
        row['sub_brand_name'] = series_nation_sales_data['sub_brand_name']
        row['min_price'] = series_nation_sales_data['min_price']
        row['max_price'] = series_nation_sales_data['max_price']
        row['dealer_price'] = series_nation_sales_data['dealer_price']
        outter_detail_type = int(series_nation_sales_data['outter_detail_type'])
        row['outter_detail_type'] = outter_detail_types[
            outter_detail_type] if outter_detail_type in outter_detail_types else 'N/A'
        row['rank'] = series_nation_sales_data['rank']
        row['last_rank'] = series_nation_sales_data['last_rank']
        row['全国'] = series_nation_sales_data['count']
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
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, exported_csv_header)
        writer.writeheader()
        writer.writerows(exported_sales_data)


def load_nation_sales_data(from_csv=False, csv_file='auto_sales_data_nation.csv'):
    if from_csv:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            loaded_nation_sales_data = list(reader)
            print('全国销量数据', len(loaded_nation_sales_data))
    else:
        # 获取全国销量数据
        loaded_nation_sales_data = get_sales_data()
        print('全国销量数据', len(loaded_nation_sales_data))
        # 将全国销量数据单独保存在csv中，csv的每行是一个车型的销量数据
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, local_csv_header)
            writer.writeheader()
            writer.writerows(loaded_nation_sales_data)
    return loaded_nation_sales_data


def load_cities_sales_data(from_csv=False, csv_file='auto_sales_data_cities.csv'):
    if from_csv:
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            city_sales_data = list(reader)
            print('城市销量数据', len(city_sales_data))
    else:
        # 获取城市列表
        cities = get_cities()
        # 按城市获取销量数据
        city_sales_data = []
        for city in cities:
            time.sleep(random.randint(1, 3))
            city_data = get_sales_data(city)
            # 打印销量数据数量
            print(city, len(city_data))
            if len(city_data) > 0:
                city_sales_data.extend(city_data)
        print('城市销量数据', len(city_sales_data))
        # 将城市销量数据单独保存在csv中，csv的每行是一个城市的销量数据
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, local_csv_header)
            writer.writeheader()
            writer.writerows(city_sales_data)
    return city_sales_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl automotive sales data.')
    parser.add_argument('-local', action='store_true', default=False, help='Load data from local csv file')
    # the default output file name, add year, month, day of today as suffix
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    parser.add_argument('-output', metavar='csv_file_name', type=str, default='auto_sales_data_' + today + '.csv',
                        help='The name of the exported csv file')

    args = parser.parse_args()
    print("Value of -local: ", args.local)
    print("Value of -output: ", args.output)

    nation_sales_data = load_nation_sales_data(args.local, 'auto_sales_data_nation_' + today + '.csv')
    cities_sales_data = load_cities_sales_data(args.local, 'auto_sales_data_cities_' + today + '.csv')
    export_sales_data_to_csv(nation_sales_data, cities_sales_data, args.output)
    print('导出成功, file_name:', args.output)
