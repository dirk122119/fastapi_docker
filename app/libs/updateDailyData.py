import requests
import pandas as pd
from dotenv import load_dotenv
import os
from loguru import logger
import time
import datetime
import pytz
import json
from rdsFunction import create_connection_pool
from loguru import logger

def getAndInsert_TwSymbol_daily(region,cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor(buffered=True)

    if(region=="TW"):
        SymbolTable="TwSymbols"
        StockTable="TwStockTable"
        Dataset="TaiwanStockPrice"
    elif(region=="US"):
        SymbolTable="UsSymbols"
        StockTable="UsStockTable"
        Dataset="USStockPrice"

    url = "https://api.finmindtrade.com/api/v4/data"
    

    sql=f"select distinct symbol from {SymbolTable};"
    cursor.execute(sql)
    symbols=cursor.fetchall()
    logger.info(symbols)
    for symbol in symbols:
        symbol=symbol[0]

        sql=f"select id from {SymbolTable} where symbol = %s;"
        val=(symbol,)
        cursor.execute(sql,val)
        symbolId=cursor.fetchone()[0]

        sql=f"select date from {StockTable} where symbol = %s ORDER BY Date DESC;"
        val=(symbolId,)
        cursor.execute(sql,val)
        last_date=cursor.fetchone()

        parameter = {
        "dataset": Dataset,
        "data_id": symbol,
        "start_date": last_date[0]+ datetime.timedelta(1),
        "end_date": datetime.datetime.now().date(),
        "token": os.getenv('FinMindTolen'), # 參考登入，獲取金鑰
        }

        for index in range(1,6,1):
            try:
                resp = requests.get(url, params=parameter)
                data = resp.json()
                data = pd.DataFrame(data["data"])
                if data.empty:
                    logger.info(f"{symbol} is latest")
                else :
                    logger.info(f"updating {symbol}")
                    logger.info(data.head())
                    for i in range (0,data.shape[0]):
                        sql=f"INSERT INTO {StockTable}(symbol,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                        if(region=="TW"):
                            val=(symbolId,data.iloc[i]["date"],data.iloc[i]["open"].item(),data.iloc[i]["max"].item(),data.iloc[i]["min"].item(),data.iloc[i]["close"].item(),data.iloc[i]["Trading_Volume"].item())
                        elif(region=="US"):
                            val=(symbolId,data.iloc[i]["date"],data.iloc[i]["Open"].item(),data.iloc[i]["High"].item(),data.iloc[i]["Low"].item(),data.iloc[i]["Close"].item(),data.iloc[i]["Volume"].item())
                        cursor.execute(sql,val)
                        connect_objt.commit()
                    logger.info(f"{symbol} update finish")
                time.sleep(3)
                break
            except Exception as e:
                logger.error(f"{symbol} error {index} time,{e}")
                logger.info("sleep 30s")
                time.sleep(30)
                logger.info("wake up ")
    cursor.close()
    connect_objt.close()
               

def get_TwSymbol_data(symbol,cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor(buffered=True)

    sql="select distinct id from TwSymbols where symbol = %s;"
    val=(symbol,)
    cursor.execute(sql,val)
    symbolId=cursor.fetchone()[0]

    sql=f"select date from TwStockTable where symbol = %s ORDER BY Date DESC;"
    val=(symbolId,)
    cursor.execute(sql,val)
    last_date=cursor.fetchone()
    logger.info(last_date[0])
    parameter = {
        "dataset": "TaiwanStockPrice",
        "data_id": symbol,
        "start_date": last_date[0]+datetime.timedelta(1),
        "end_date": datetime.datetime.now().date(),
        "token": os.getenv('FinMindTolen'), # 參考登入，獲取金鑰
        }
    url = "https://api.finmindtrade.com/api/v4/data"
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor(buffered=True)

    if data.empty:
        logger.info(f"{symbol} is latest")
    else :
        logger.info(f"updating {symbol}")
        logger.info(data.head())
        logger.info(data.iloc[0]["Trading_Volume"])
        logger.info(f"{symbol} update finish")
    cursor.close()
    connect_objt.close()

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


if __name__ == '__main__':
    load_dotenv()
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    est = pytz.timezone('EST')
    getAndInsert_TwSymbol_daily("TW",cnx)
    # getAndInsert_TwSymbol_daily("US",cnx)