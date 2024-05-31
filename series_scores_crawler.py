import argparse
import csv
import time
import requests

from constants import SCORE_TYPE_LIST, UTF_SIG
from series_scores import SeriesScores

# 懂车分榜
RANK_SCORE_URL = ('https://www.dongchedi.com/motor/pc/car/rank_data?aid=1839&app_name=auto_web_pc&city_name=&count={}'
                  '&offset={}&month=&new_energy_type=&rank_data_type={}'
                  '&brand_id=&price=&manufacturer=&outter_detail_type=&nation=0')

# local csv header for automotive sales data
LOCAL_CSV_HEADER = ['series_id', 'series_name', 'brand_id', 'brand_name', 'sub_brand_id', 'sub_brand_name',
                    'overall_score', 'overall_rank', 'comfort_score', 'comfort_rank', 'exterior_score', 'exterior_rank',
                    'interior_score', 'interior_rank', 'configuration_score', 'configuration_rank', 'control_score',
                    'control_rank', 'power_score', 'power_rank', 'space_score', 'space_rank']


class SeriesScoresCrawler:
    def __init__(self):
        self.series_scores = {}

    def get_series_scores(self):
        for score_type in SCORE_TYPE_LIST:
            self.get_series_score_by_type(score_type)

    def get_series_score_by_type(self, score_type):
        page_size = 1000
        offset = 0
        data_count = 1000
        while data_count == page_size:
            url = RANK_SCORE_URL.format(page_size, offset, score_type)
            response = requests.get(url)
            json_data = response.json()
            data_count = len(json_data['data']['list']) if json_data['data']['list'] else 0
            if data_count > 0:
                for item in json_data['data']['list']:
                    if item['series_id'] not in self.series_scores:
                        self.series_scores[item['series_id']] = SeriesScores.from_json(score_type, item)
                    else:
                        self.series_scores[item['series_id']].update_score_rank(score_type, item)
            offset += page_size

    def export_score_rank_to_csv(self, csv_file='score_rank_data.csv'):
        csv_rows = []
        for series_score in self.series_scores.values():
            row = {'series_id': series_score.series_id, 'brand_id': series_score.brand_id,
                   'brand_name': series_score.brand_name, 'sub_brand_id': series_score.sub_brand_id,
                   'sub_brand_name': series_score.sub_brand_name, 'series_name': series_score.series_name}
            for score_type in SCORE_TYPE_LIST:
                score_name = SCORE_TYPE_LIST[score_type] + '_score'
                rank_name = SCORE_TYPE_LIST[score_type] + '_rank'
                row[score_name] = series_score.scores[score_type]
                row[rank_name] = series_score.ranks[score_type]
            csv_rows.append(row)

        with open(csv_file, 'w', newline='', encoding=UTF_SIG) as f:
            writer = csv.DictWriter(f, LOCAL_CSV_HEADER)
            writer.writeheader()
            writer.writerows(csv_rows)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl series score data.')
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    parser.add_argument('-output', metavar='csv_file_name', type=str, default='score_rank_data_' + today + '.csv',
                        help='The name of the local csv file')

    args = parser.parse_args()
    print("Value of -output: ", args.output)

    crawler = SeriesScoresCrawler()
    crawler.get_series_scores()
    crawler.export_score_rank_to_csv(args.output)

    print('导出成功, file_name:', args.output)
