import datetime
import requests
import json
from connectMySQL import connect
import time
import statistics

class stock_info():
    def __init__(self, name):
        self.name = name

    def getMA(stock_id, days):
        data_ma_tuple = connect.query_list("SELECT close FROM stock.stock_master where stock_id=" + stock_id + " order by date desc limit "+ days)
        print (data_ma_tuple)
        data_ma = list()
        for close in data_ma_tuple:
            data_ma.append(close[0])

        return statistics.mean(data_ma)



