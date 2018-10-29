import datetime
import requests
import json
from connectMySQL import connect
import time

class crawler():
    def __init__(self, name):
        self.name = name

    def getStock(stockid, year, monthStart, monthEnd):
        # get datetime for get stock
        now = datetime.datetime.now()
        now = now.strftime("%Y%m%d")
        #res = requests.get(
        #   'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + str(now) + '&stockNo=' + stockid)
        #   http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=20181025&stockNo=3665

        for j in range(monthStart, monthEnd+1):
            jStr = '0'
            if(j<10):
                jStr += str(j)
            else:
                jStr = str(j)
            print(str(year)+jStr)

            res = requests.get(
            'http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=' + str(year) + jStr + '01' + '&stockNo=' + stockid)
            json_data = json.loads(res.text)
            monthInfoArray = json_data['data']

            #connect.create_database()
            #connect.create_table()

            for dayInfo in monthInfoArray:
                # transfer date(107 + 1911 -> 2018)
                dateStr = dayInfo[0].split("/")
                dateStr[0] = str(int(dateStr[0]) + 1911)
                dateStr = datetime.datetime.strptime('/'.join(dateStr), '%Y/%m/%d')

                print(dateStr)

                #transfer
                open = dayInfo[3].replace(",", "").replace(" ", "")
                if "--" in open:
                    open = None
                else:
                    open = float(open)

                high = dayInfo[4].replace(",", "").replace(" ", "")
                if "--" in high:
                    high = None
                else:
                    high = float(high)

                low = dayInfo[5].replace(",", "").replace(" ", "")
                if "--" in low:
                    low = None
                else:
                    low = float(low)

                close = dayInfo[6].replace(",", "").replace(" ", "")
                if "--" in close:
                    close = None
                else:
                    close = float(close)

                advance_decline = dayInfo[7].replace(",", "").replace(" ", "")
                if "X" in advance_decline:
                    advance_decline = None
                else:
                    advance_decline = float(advance_decline)
                # insert stock row
                data_stock = {
                    'stock_id': stockid,
                    'date': dateStr,
                    'trading_volume': int(dayInfo[1].replace(",", "").replace(" ", "")),
                    'turnover_in_value': int(dayInfo[2].replace(",", "").replace(" ", "")),
                    'open': open,
                    'high': high,
                    'low': low,
                    'close': close,
                    'advance_decline': advance_decline,
                    'transaction_count': int(dayInfo[8].replace(",", "").replace(" ", "")),
                }

                add_stock = ("INSERT INTO stock_master "
                             "(stock_id, date, trading_volume, turnover_in_value,"
                             "open, high, low, close, advance_decline, transaction_count) "
                             "VALUES (%(stock_id)s, %(date)s, %(trading_volume)s, %(turnover_in_value)s,"
                             "%(open)s, %(high)s, %(low)s, %(close)s,"
                             "%(advance_decline)s, %(transaction_count)s)")
                connect.add_row(add_stock, data_stock)

        return str(data_stock)

