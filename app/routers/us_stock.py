from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
import datetime
from  app.libs.rdsFunction import create_connection_pool

router=APIRouter()

@router.get("/us_stock", tags=["us_stock"])
def us_stock_index():
    return {"now in us_stock_index"}


@router.get("/us_stock/get_all_symbol_OCHL", tags=["us_stock"])
def get_us_all_symbol_OCHL():
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT MAX(UsStockTable.date) AS latest_date,UsSymbols.symbol,UsStockTable.open,UsStockTable.high,UsStockTable.low,UsStockTable.close,UsSymbols.companyName from UsStockTable INNER JOIN UsSymbols ON UsStockTable.symbol=UsSymbols.id GROUP BY symbol;"
    cursor.execute(sql)
    data=cursor.fetchall()
    data_list=[]
    for row in data:
        data_list.append({"symbol":row[1],"company name":row[6],"latest_date":row[0],"open":row[2],"high":row[3],"close":row[5],"low":row[4]})
    
    cursor.close()
    connect_objt.close()
    return {"data":data_list}

@router.get("/us_stock/get_us_all_symbol", tags=["us_stock"])
def get_us_all_symbol():
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT symbol,companyName from UsSymbols;"
    cursor.execute(sql)
    data=cursor.fetchall()
    data_list=[]
    for row in data:
         data_list.append({"symbol":row[0],"company name":row[1]})
    return {"symbol":data_list}