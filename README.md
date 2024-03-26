# Crawl automotive sales data

## Python version
`
python3.9
`

## Installation the necessary packages.
`
pip3 install -r requirements.txt
`

## Usage
Run the script with the following command, and the automotive sales data will be saved to a csv file named `auto_sales_data.csv` in the current directory.  
```
python3 crawl_auto_sales_data.py
```

You can specify the following command line options:  
- `-local`: Load data from local csv file. If this option is present, the script will load data from a local csv files (`auto_sales_data_nation.csv` and `auto_sales_data_cities.csv`). If not, the script will load data from DongCheDi dot com, and after load data, the script will save the automotive sales data into local csv files (`auto_sales_data_nation.csv` and `auto_sales_data_cities.csv`).  
- `-o csv_file_name`: The name of the exported csv file. Replace `csv_file_name` with the name of the csv file you want to export. **The default value is `auto_sales_data.csv`**.  

## Examples
### Case 1:
In this example, you can rename the output csv file name by `-o` option, the script will load data from DongCheDi dot com (because `-local` is not present) and export the data to a file named `output.csv`.
```
python3 crawl_auto_sales_data.py -o output.csv
```
### Case 2:
In this example, if you already load the data from DongCheDi dot com and already saved the data into local csv files (`auto_sales_data_nation.csv` and `auto_sales_data_cities.csv`), you just want to change the script to reformat the exported csv file, you can use the following command.  
Fetching all sales data from the internet will take approximately 5-10 minutes. Therefore, if the data has already been fetched and saved locally, it is recommended to add the -local option. This will significantly reduce the script's execution time and avoid unnecessary data retrieval.   
```
python3 crawl_auto_sales_data.py -local -o output.csv
```
