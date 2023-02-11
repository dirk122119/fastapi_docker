from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
import datetime
from  app.libs.rdsFunction import create_connection_pool

router=APIRouter()

@router.get("/tw_stock", tags=["tw_stock"])
def Tw_stock_index():
    return {"now in Tw_stock_index"}


@router.get("/tw_stock/get_all_symbol_OCHL", tags=["tw_stock"])
def get_tw_all_symbol_OCHL():
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT MAX(TwStockTable.date) AS latest_date,TwSymbols.symbol,TwStockTable.open,TwStockTable.high,TwStockTable.low,TwStockTable.close,TwSymbols.companyName from TwStockTable INNER JOIN TwSymbols ON TwStockTable.symbol=TwSymbols.id GROUP BY symbol;"
    cursor.execute(sql)
    data=cursor.fetchall()
    data_list=[]
    for row in data:
        data_list.append({"symbol":row[1],"company name":row[6],"latest_date":row[0],"open":row[2],"high":row[3],"close":row[5],"low":row[4]})
    
    cursor.close()
    connect_objt.close()
    return {"data":data_list}