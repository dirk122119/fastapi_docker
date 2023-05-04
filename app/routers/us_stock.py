from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
from datetime import datetime,timedelta
import pytz
from fastapi.responses import JSONResponse
from  app.libs.rdsFunction import create_connection_pool

router=APIRouter()

# @router.get("/us_stock", tags=["us_stock"])
# def us_stock_index():
#     return {"now in us_stock_index"}

# @router.get("/us_stock/get_all_symbol_OCHL", tags=["us_stock"])
# def get_us_all_symbol_OCHL():
#     try:
#         cnx=create_connection_pool()
#     except:
#         print("無法建立connect pool")
#     connect_objt=cnx.get_connection()
#     cursor = connect_objt.cursor()
#     sql="SELECT MAX(UsStockTable.date) AS latest_date,UsSymbols.symbol,UsStockTable.open,UsStockTable.high,UsStockTable.low,UsStockTable.close,UsSymbols.companyName from UsStockTable INNER JOIN UsSymbols ON UsStockTable.symbol=UsSymbols.id GROUP BY symbol;"
#     cursor.execute(sql)
#     data=cursor.fetchall()
#     data_list=[]
#     for row in data:
#         data_list.append({"symbol":row[1],"company name":row[6],"latest_date":row[0],"open":row[2],"high":row[3],"close":row[5],"low":row[4]})
    
#     cursor.close()
#     connect_objt.close()
#     return {"data":data_list}

@router.get("/us_stock/get_us_all_symbol", tags=["us_stock"])
def get_us_all_symbol():
    url = 'https://api.finmindtrade.com/api/v4/data'
    token=os.getenv('FinMindTolen')
    parameter = {
        "dataset": "USStockInfo",
        "token": token,
    }
    data = requests.get(url, params=parameter)
    data = data.json()
    data = pd.DataFrame(data['data'])
    data_list=[]
    for symbol in data.itertuples():
        data_list.append({"symbol":symbol.stock_id,"company name":symbol.stock_name})
        
    response=JSONResponse(status_code=200, content={"symbol":data_list})
    return response

@router.get("/us_stock/get_symbol_OHCL", tags=["us_stock"])
def get_symbol_OHCL(symbol:str):


    url = 'https://api.finmindtrade.com/api/v4/data'
    token=os.getenv('FinMindTolen')

    mytz = pytz.timezone('Asia/Taipei')
    time_for_now = datetime.now().replace(tzinfo=mytz)
    time_before_30days = time_for_now - timedelta(days = 30)
    
    parameter = {
        "dataset": "USStockPrice",
        "data_id": symbol,
        "start_date":  time_before_30days.strftime("%Y-%m-%d"),
        "end_date": time_for_now.strftime("%Y-%m-%d"),
        "token": token, # 參考登入，獲取金鑰
    }
    data = requests.get(url, params=parameter)
    data = data.json()
    data = pd.DataFrame(data['data'])
    data_list=[]
    for target in data.itertuples():
        data_list.append({"symbol":target.stock_id,"date":target.date,"open":target.Open,"high":target.High,"low":target.Low,"close":target.Close,"volume":target.Volume})
    
    response=JSONResponse(status_code=200, content={"data":data_list})
    return response