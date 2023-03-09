from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
import datetime
from  app.libs.rdsFunction import create_connection_pool
from fastapi.responses import JSONResponse

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

@router.get("/tw_stock/get_tw_all_symbol", tags=["tw_stock"])
def get_tw_all_symbol():
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT symbol,companyName from TwSymbols;"
    cursor.execute(sql)
    data=cursor.fetchall()
    data_list=[]
    cursor.close()
    connect_objt.close()
    for row in data:
         data_list.append({"symbol":row[0],"company name":row[1]})
    return {"symbol":data_list}

@router.get("/tw_stock/get_symbol_OHCL", tags=["tw_stock"])
def get_symbol_OHCL(symbol:str):
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT TwSymbols.id,TwSymbols.symbol,TwStockTable.date,TwStockTable.open,TwStockTable.high,TwStockTable.low,TwStockTable.close,TwStockTable.volume from TwStockTable INNER JOIN TwSymbols ON TwStockTable.symbol=TwSymbols.id WHERE TwSymbols.symbol = %s AND TwStockTable.date >=  CURDATE() - INTERVAL 30 DAY;"
    val=(symbol,)
    cursor.execute(sql,val)
    data=cursor.fetchall()
    data_list=[]
    cursor.close()
    connect_objt.close()
    for row in data:
        data_list.append({"symbol":row[1],"date":str(row[2]),"open":row[3],"high":row[4],"low":row[5],"close":row[6],"volume":row[7]})
    response=JSONResponse(status_code=200, content={"data":data_list})
    return response