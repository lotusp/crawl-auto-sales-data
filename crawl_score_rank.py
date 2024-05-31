import argparse
import csv
import time
import requests

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


class SeriesScore:
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


class ScoreRankCrawler:
    def __init__(self):
        self.series_scores = {}

    def get_series_scores(self):
        for score_type in score_type_list:
            self.get_series_score_by_type(score_type)

    def get_series_score_by_type(self, score_type):
        page_size = 1000
        offset = 0
        data_count = 1000
        while data_count == page_size:
            url = rank_score_url.format(page_size, offset, score_type)
            response = requests.get(url)
            json_data = response.json()
            data_count = len(json_data['data']['list']) if json_data['data']['list'] else 0
            if data_count > 0:
                for item in json_data['data']['list']:
                    if item['series_id'] not in self.series_scores:
                        self.series_scores[item['series_id']] = SeriesScore.from_json(score_type, item)
                    else:
                        self.series_scores[item['series_id']].update_score_rank(score_type, item)
            offset += page_size

    def export_score_rank_to_csv(self, csv_file='score_rank_data.csv'):
        csv_rows = []
        for series_score in self.series_scores.values():
            row = {'series_id': series_score.series_id, 'brand_id': series_score.brand_id,
                   'brand_name': series_score.brand_name, 'sub_brand_id': series_score.sub_brand_id,
                   'sub_brand_name': series_score.sub_brand_name, 'series_name': series_score.series_name}
            for score_type in score_type_list:
                score_name = score_type_list[score_type] + '_score'
                rank_name = score_type_list[score_type] + '_rank'
                row[score_name] = series_score.scores[score_type]
                row[rank_name] = series_score.ranks[score_type]
            csv_rows.append(row)

        with open(csv_file, 'w', newline='', encoding=utf_sig) as f:
            writer = csv.DictWriter(f, local_csv_header)
            writer.writeheader()
            writer.writerows(csv_rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl series score data.')
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    parser.add_argument('-output', metavar='csv_file_name', type=str, default='score_rank_data_' + today + '.csv',
                        help='The name of the local csv file')

    args = parser.parse_args()
    print("Value of -output: ", args.output)

    crawler = ScoreRankCrawler()
    crawler.get_series_scores()
    crawler.export_score_rank_to_csv(args.output)

    print('导出成功, file_name:', args.output)
