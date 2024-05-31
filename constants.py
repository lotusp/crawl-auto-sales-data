# csv文件编码
UTF_SIG = 'utf-8-sig'

#  0-微型车，1-小型车，2-紧凑型车，3-中型车，4-中大型车，5-大型车
#  10-小型SUV，11-紧凑型SUV，12-中型SUV，13-中大型SUV，14-大型SUV
#  20-小型MPV，21-紧凑型MPV，22-中型MPV，23-中大型MPV，24-大型MPV
OUTTER_DETAIL_TYPES = {
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
NEW_ENERGY_TYPES = {
    0: 'N/A',
    1: '纯电动',
    2: '插电式混动',
    3: '增程式'
}

# 懂车分榜
SCORE_TYPE_LIST = {
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
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
}
