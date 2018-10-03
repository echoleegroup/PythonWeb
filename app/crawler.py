import datetime
import requests
import json

class crawler():
    def __init__(self, name):
        self.name = name

    def getStock2327():
        # get datetime for get stock
        now = datetime.datetime.now()
        now = now.strftime("%Y%m%d")
        res = requests.get(
            'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + str(now) + '&stockNo=2327')
        json_data = json.loads(res.text)
        msgArray = json_data['data']
        print(msgArray[-1])
        return str(msgArray[-1])

    def getStock2330():
        # get datetime for get stock
        now = datetime.datetime.now()
        now = now.strftime("%Y%m%d");
        res = requests.get(
            'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + str(now) + '&stockNo=2330')
        json_data = json.loads(res.text)
        msgArray = json_data['data']
        print(msgArray[-1][-1])
        return str(msgArray[-1][-1])

