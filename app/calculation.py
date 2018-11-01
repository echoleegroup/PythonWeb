import datetime
import requests
import json
from connectMySQL import connect
import time
import statistics
import pandas as pd

def calculateDayLineUtils(stock_id, limitNumber):
    data_ma_tuple = connect.query_list(
        "SELECT close, date FROM stock.stock_master where stock_id=" + stock_id + " order by date desc limit " + limitNumber)
    obj_ma = connect.transTupleToObject(data_ma_tuple, ['close', 'date'])
    close_data = obj_ma['close']
    df_ma = pd.DataFrame(obj_ma)
    for days in [5, 10, 20, 60, 120, 240]:
        i = 0
        days_value = []
        date_value = []
        for i in range(0, len(close_data) - days, +1):
            cur_ma = close_data[i:i + days]
            if cur_ma.count(None) > 0:
                break
            days_value.append(statistics.mean(cur_ma))
            date_value.append(obj_ma['date'][i])
        days_df = pd.DataFrame({str(days) + '_days': days_value, 'date': date_value})
        df_ma = df_ma.merge(days_df, how='left', left_on='date', right_on='date')
    # add stock_id column
    df_ma['stock_id'] = stock_id
    return df_ma

class stock_info():
    def __init__(self, name):
        self.name = name

    def getMA(stock_id, days):
        data_ma_tuple = connect.query_list("SELECT close FROM stock.stock_master where stock_id=" + stock_id + " and close is not null order by date desc limit "+ days)
        data_ma = connect.transTupleToList(data_ma_tuple, 0)
        return statistics.mean(data_ma)

    def calculateStockDayLine(stock_id, today):
        df_ma = calculateDayLineUtils(stock_id, 1000)
        '''
        data_ma_tuple = connect.query_list(
            "SELECT close, date FROM stock.stock_master where stock_id=" + stock_id + " order by date desc limit 1000")
        obj_ma = connect.transTupleToObject(data_ma_tuple, ['close', 'date'])
        close_data = obj_ma['close']
        df_ma = pd.DataFrame(obj_ma)
        for days in [5, 10, 20, 60, 120, 240]:
            i = 0
            days_value = []
            date_value = []
            for i in range(0, len(close_data) - days, +1):
                cur_ma = close_data[i:i + days]
                if cur_ma.count(None) > 0:
                    break
                days_value.append(statistics.mean(cur_ma))
                date_value.append(obj_ma['date'][i])
            days_df = pd.DataFrame({str(days) + '_days': days_value, 'date': date_value})
            df_ma = df_ma.merge(days_df, how='left', left_on='date', right_on='date')
       
        # add stock_id column
        df_ma['stock_id'] = stock_id
        '''
        df_ma = df_ma[df_ma['date'] > today]
        engine = connect.createEngine()
        df_ma[['stock_id', 'date', '5_days', '10_days', '20_days', '60_days', '120_days', '240_days']] \
            .to_sql(name='stock_days', con=engine, if_exists='append', index=False)
        return "SUCCESSFUL"

    def calculateDayLine():
        stock_list_tuple = connect.query_list("SELECT stock_id FROM stock.stock_list")
        stock_list = connect.transTupleToList(stock_list_tuple, 0)

        for stock_id in stock_list:
            df_ma = calculateDayLineUtils(stock_id, 10000)
            '''
            data_ma_tuple = connect.query_list(
                "SELECT close, date FROM stock.stock_master where stock_id=" + stock_id + " order by date desc limit 10000")
            obj_ma = connect.transTupleToObject(data_ma_tuple, ['close', 'date'])
            close_data = obj_ma['close']
            df_ma = pd.DataFrame(obj_ma)
            for days in [5, 10, 20, 60, 120, 240]:
                i = 0
                days_value = []
                date_value = []
                for i in range(0, len(close_data) - days, +1):
                    cur_ma = close_data[i:i + days]
                    if cur_ma.count(None) > 0:
                        break
                    days_value.append(statistics.mean(cur_ma))
                    date_value.append(obj_ma['date'][i])
                days_df = pd.DataFrame({str(days)+'_days': days_value, 'date': date_value})
                df_ma = df_ma.merge(days_df, how='left', left_on = 'date', right_on='date')
            df_ma['stock_id'] = stock_id
            '''
            engine = connect.createEngine()
            df_ma[['stock_id', 'date', '5_days', '10_days', '20_days', '60_days', '120_days', '240_days']]\
                .to_sql(name='stock_days', con=engine, if_exists='append', index=False)
        return "SUCCESSFUL"
