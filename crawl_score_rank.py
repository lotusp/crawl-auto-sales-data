import requests
import csv
import time
import random
import argparse

# csv文件编码
utf_sig = 'utf-8-sig'

# 懂车分榜
score_type_list = {
    58: 'overall',
    59: 'comfort',
    51: 'exterior',
    57: 'interior',
    53: 'configuration',
    54: 'control',
    55: 'power',
    56: 'space'
}

# request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}

# 懂车分榜
rank_score_url = 'https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=&count={}&offset={}&month=&new_energy_type=&rank_data_type={}&brand_id=&price=&manufacturer=&outter_detail_type=&nation=0'

# local csv header for automotive sales data
local_csv_header = ['series_id', 'series_name', 'brand_id', 'brand_name', 'sub_brand_id', 'sub_brand_name',
                    'overall_score', 'overall_rank', 'comfort_score', 'comfort_rank', 'exterior_score', 'exterior_rank',
                    'interior_score', 'interior_rank', 'configuration_score', 'configuration_rank', 'control_score',
                    'control_rank', 'power_score', 'power_rank', 'space_score', 'space_rank']

#
def get_series_scores(score_type: int):
    page_size = 1000
    offset = 0
    data_count = 1000
    # 逐页获取销量数据
    series_score_list = []
    while data_count == page_size:
        url = rank_score_url.format(page_size, offset, score_type)
        response = requests.get(url)
        json_data = response.json()
        data_count = len(json_data['data']['list']) if json_data['data']['list'] else 0
        if data_count > 0:
            rank_data = parse_series_score(json_data, score_type)
            series_score_list.extend(rank_data)
        offset += page_size
    return series_score_list

# 从json中提取数据
def parse_series_score(json_data, score_type):
    series_scores = []
    for item in json_data['data']['list']:
        series_scores.append({
            'series_id': item['series_id'],
            'brand_id': item['brand_id'],
            'brand_name': item['brand_name'],
            'sub_brand_id': item['sub_brand_id'],
            'sub_brand_name': item['sub_brand_name'],
            'series_name': item['series_name'],
            'score_type': score_type,
            'rank': item['rank'],
            'score': float(item['score'])/100
        })
    return series_scores

def get_all_scores():
    all_series_scores = []
    for score_type in score_type_list:
        all_series_scores.extend(get_series_scores(score_type))
    return all_series_scores

# 导出销量数据到csv中
def export_score_rank_to_csv(series_score_list, csv_file='score_rank_data.csv'):
    series_score_map = {}
    for item in series_score_list:
        series_id = int(item['series_id'])
        if series_id not in series_score_map:
            series_score_map[series_id] = {}
            series_score_map[series_id]['series_id'] = series_id
            series_score_map[series_id]['series_name'] = item['series_name']
            series_score_map[series_id]['brand_id'] = item['brand_id']
            series_score_map[series_id]['brand_name'] = item['brand_name']
            series_score_map[series_id]['sub_brand_id'] = item['sub_brand_id']
            series_score_map[series_id]['sub_brand_name'] = item['sub_brand_name']
        score_name = score_type_list[item['score_type']] + '_score'
        rank_name = score_type_list[item['score_type']] + '_rank'
        series_score_map[series_id][score_name] = item['score']
        series_score_map[series_id][rank_name] = item['rank']

    # 写入csv文件
    with open(csv_file, 'w', newline='', encoding=utf_sig) as f:
        writer = csv.DictWriter(f, local_csv_header)
        writer.writeheader()
        writer.writerows(series_score_map.values())

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl series score data.')
    # the default output file name, add year, month, day of today as suffix
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    parser.add_argument('-output', metavar='csv_file_name', type=str, default='score_rank_data_' + today + '.csv',
                        help='The name of the local csv file')

    args = parser.parse_args()
    print("Value of -output: ", args.output)

    series_score_list = get_all_scores()
    export_score_rank_to_csv(series_score_list, args.output)

    print('导出成功, file_name:', args.output)
