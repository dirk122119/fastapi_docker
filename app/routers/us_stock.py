from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
import datetime
from fastapi.responses import JSONResponse
from  app.libs.rdsFunction import create_connection_pool

router=APIRouter()

# @router.get("/us_stock", tags=["us_stock"])
# def us_stock_index():
#     return {"now in us_stock_index"}


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

@router.get("/us_stock/get_symbol_OHCL", tags=["us_stock"])
def get_symbol_OHCL(symbol:str):
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="SELECT UsSymbols.companyName,UsSymbols.symbol,UsStockTable.date,UsStockTable.open,UsStockTable.high,UsStockTable.low,UsStockTable.close,UsStockTable.volume from UsStockTable INNER JOIN UsSymbols ON UsStockTable.symbol=UsSymbols.id WHERE UsSymbols.symbol = %s AND UsStockTable.date >=  CURDATE() - INTERVAL 30 DAY;"
    val=(symbol,)
    cursor.execute(sql,val)
    data=cursor.fetchall()
    data_list=[]
    cursor.close()
    connect_objt.close()
    df = pd.DataFrame(data)
    df = df.drop_duplicates(subset=[2], keep='first')
    for i in range (0,df.shape[0]):
        data_list.append({"companyName":df.iloc[i][0],"symbol":df.iloc[i][1],"date":str(df.iloc[i][2]),"open":df.iloc[i][3],"high":df.iloc[i][4],"low":df.iloc[i][5],"close":df.iloc[i][6],"volume":df.iloc[i][7]})
   
    response=JSONResponse(status_code=200, content={"data":data_list})
    return response