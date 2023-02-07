import requests
import pandas as pd
from dotenv import load_dotenv
import os
from loguru import logger
import time
from rdsFunction import create_connection_pool

def get_symbol_history_price(data_id,start_date,end_date,token,cnx):
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
    
    



def get_all_symbol_history_data(start_date,end_date,token,cnx):
    symbols = pd.read_csv("./tw_0050_0051_list.csv")["symbol"]
    for symbol in symbols:
        for index in range(1,6,1):
            try:
                connect_objt=cnx.get_connection()
                cursor = connect_objt.cursor(buffered=True)
                sql="select id from TwSymbols WHERE symbol = %s"
                val=(symbol,)
                cursor.execute(sql,val)
                symbolId=cursor.fetchone()
                print(symbolId)
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
                print("sleep 11s")
                time.sleep(11)
                print("wake up")
                break

load_dotenv()

try:
    cnx=create_connection_pool()
except:
    print("無法建立connect pool")

# get_all_symbol_history_data("2000-01-01","2023-01-31",os.getenv('FinMindTolen'),cnx)

