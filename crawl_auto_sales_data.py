import argparse
import time

from auto_series_sales_crawler import AutoSalesCrawler

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

    auto_sales_data_crawler = AutoSalesCrawler()
    auto_sales_data_crawler.load_sales_data(args.local)
    auto_sales_data_crawler.export_sales_data_to_csv(args.output)
    print('导出成功, file_name:', args.output)
