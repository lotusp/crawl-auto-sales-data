import argparse
import time

from series_scores_crawler import SeriesScoresCrawler

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Crawl series score data.')
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    parser.add_argument('-output', metavar='csv_file_name', type=str, default='score_rank_data_' + today + '.csv',
                        help='The name of the local csv file')

    args = parser.parse_args()
    print("Value of -output: ", args.output)

    crawler = SeriesScoresCrawler()
    crawler.crawl_series_scores()
    crawler.export_score_rank_to_csv(args.output)

    print('导出成功, file_name:', args.output)
