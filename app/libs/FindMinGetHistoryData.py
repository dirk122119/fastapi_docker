import requests
import pandas as pd
from dotenv import load_dotenv
import os
from loguru import logger
import time
from rdsFunction import create_connection_pool

def get_tw_symbol_history_price(data_id,start_date,end_date,token,cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="select id from TwSymbols WHERE symbol = %s"
    val=(data_id,)
    cursor.execute(sql,val)
    symbolId=cursor.fetchone()
    logger.info(symbolId[0])
        
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
    "dataset": "TaiwanStockPrice",
    "data_id": data_id,
    "start_date": start_date,
    "end_date": end_date,
    "token": token, # 參考登入，獲取金鑰
    }
    print(f"get {data_id} data")
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    logger.info(data)
    for i in range (0,data.shape[0]):
        sql=f"INSERT INTO TwStockTable(symbol,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        val=(symbolId[0],data.iloc[i]["date"],data.iloc[i]["open"].item(),data.iloc[i]["max"].item(),data.iloc[i]["min"].item(),data.iloc[i]["close"].item(),data.iloc[i]["Trading_Volume"].item())
        cursor.execute(sql,val)
        connect_objt.commit()
    cursor.close()
    connect_objt.close()
    

def get_tw_all_symbol_history_data(start_date,end_date,token,cnx):
    symbols = pd.read_csv("./tw_symbol_list.csv")["stock_id"]
    for symbol in symbols:
        for index in range(1,6,1):
            try:
                connect_objt=cnx.get_connection()
                cursor = connect_objt.cursor(buffered=True)
                sql="select id from TwSymbols WHERE symbol = %s"
                val=(symbol,)
                cursor.execute(sql,val)
                symbolId=cursor.fetchone()
                print(f"get ID:{symbolId} company:{symbol}")
                url = "https://api.finmindtrade.com/api/v4/data"
                parameter = {
                "dataset": "TaiwanStockPrice",
                "data_id": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "token": token, # 參考登入，獲取金鑰
                }
                print(f"get {symbol} data")
                resp = requests.get(url, params=parameter)
                data = resp.json()
                data = pd.DataFrame(data["data"])
                logger.info(data)
                for i in range (0,data.shape[0]):
                    sql=f"INSERT INTO TwStockTable(symbol,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                    val=(symbolId[0],data.iloc[i]["date"],data.iloc[i]["open"].item(),data.iloc[i]["max"].item(),data.iloc[i]["min"].item(),data.iloc[i]["close"].item(),data.iloc[i]["Trading_Volume"].item())
                    cursor.execute(sql,val)
                    connect_objt.commit()
                cursor.close()
                connect_objt.close()
                
            except Exception as e:
                logger.error(f"{symbol} error {index} time,{e}")
            finally:
                print("sleep 1s")
                time.sleep(1)
                print("wake up")
                break

def get_us_all_symbol_history_data(start_date,end_date,token,cnx):
    symbols = pd.read_csv("./us_symbol_list.csv")["stock_id"]
    for symbol in symbols:
        for index in range(1,6,1):
            try:
                connect_objt=cnx.get_connection()
                cursor = connect_objt.cursor(buffered=True)
                sql="select id from UsSymbols WHERE symbol = %s"
                val=(symbol,)
                cursor.execute(sql,val)
                symbolId=cursor.fetchone()
                print(f"get ID:{symbolId} company:{symbol}")
                url = "https://api.finmindtrade.com/api/v4/data"
                parameter = {
                "dataset": "USStockPrice",
                "data_id": symbol,
                "start_date": start_date,
                "end_date": end_date,
                "token": token, # 參考登入，獲取金鑰
                }
                print(f"get {symbol} data")
                resp = requests.get(url, params=parameter)
                data = resp.json()
                data = pd.DataFrame(data["data"])
                logger.info(data)
                for i in range (0,data.shape[0]):
                    sql=f"INSERT INTO UsStockTable(symbol,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
                    val=(symbolId[0],data.iloc[i]["date"],data.iloc[i]["Open"].item(),data.iloc[i]["High"].item(),data.iloc[i]["Low"].item(),data.iloc[i]["Close"].item(),data.iloc[i]["Volume"].item())
                    cursor.execute(sql,val)
                    connect_objt.commit()
                cursor.close()
                connect_objt.close()
                
            except Exception as e:
                logger.error(f"{symbol} error {index} time,{e}")
            finally:
                print("sleep 3s")
                time.sleep(3)
                print("wake up")
                break

def get_tw_all_symbol():
    load_dotenv()
    token=os.getenv('FinMindTolen')
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
    "dataset": "TaiwanStockInfo",
    "token": token, # 參考登入，獲取金鑰
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    data.to_csv("tw_symbol_list.csv",index=False)

def get_us_all_symbol():
    load_dotenv()
    token=os.getenv('FinMindTolen')
    url = "https://api.finmindtrade.com/api/v4/data"
    parameter = {
    "dataset": "USStockInfo",
    "token": token, # 參考登入，獲取金鑰
    }
    resp = requests.get(url, params=parameter)
    data = resp.json()
    data = pd.DataFrame(data["data"])
    data.to_csv("us_symbol_list.csv",index=False)

if __name__ == '__main__':
    load_dotenv()
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")
    get_tw_all_symbol_history_data("2000-01-01","2023-03-7",os.getenv('FinMindTolen'),cnx)

