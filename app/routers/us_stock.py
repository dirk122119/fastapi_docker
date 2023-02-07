from fastapi import APIRouter
import requests
import os
from loguru import logger
import pandas as pd
import datetime

router=APIRouter()

@router.get("/us_stock", tags=["us_stock"])
def us_stock_index():
    return {"now in us_stock_index"}

@router.get("/us_stock/get_dashboard_index", tags=["us_stock"])
def get_dow_sp500_nasdaq():
    url = 'https://api.finmindtrade.com/api/v4/data'
    parameter = { "DJI":{
    "dataset": "USStockPriceMinute",
    "data_id": "^DJI",
    "start_date": "2022-02-3",
    "token": os.getenv('FinMindTolen'),
    },"SP500":{
        "dataset": "USStockPriceMinute",
        "data_id": "^GSPC",
        "start_date": "2022-02-3",
        "token": os.getenv('FinMindTolen'),
    },"QQQ":{
        "dataset": "USStockPriceMinute",
        "data_id": "^IXIC",
        "start_date": "2022-02-3",
        "token": os.getenv('FinMindTolen'),
    }}
    data = requests.get(url, params=parameter["QQQ"])
    data = data.json()
    data = pd.DataFrame(data['data'])
    print(data.iloc[-1])
    