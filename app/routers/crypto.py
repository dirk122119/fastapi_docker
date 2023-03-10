from fastapi import APIRouter
import requests
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import json
import pandas as pd
import functools
import operator
import datetime
import pytz
from loguru import logger
router=APIRouter()

# @router.get("/crypto", tags=["crypto"])
# def crypto_index():
#     return {"crypto index"}

@router.get("/crypto/top7_search", tags=["crypto"])
async def get_coingecko_top7_search():
    res = requests.get('https://api.coingecko.com/api/v3/search/trending')

    return res.json()

@router.get("/crypto/sparkline/{coin}",tags=["crypto"])
async def get_1d_sparkline(coin):
    chart = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart?vs_currency=usd&days=1')

    data=functools.reduce(operator.iconcat, chart.json()["prices"], [])
    time_series=data[::2]
    prices_series_24h=data[1::2]
    time_series_24h=[]
    for time in time_series:
        dt_utc_aware = datetime.datetime.fromtimestamp(time/1000, pytz.timezone("Asia/Taipei"))
        time_series_24h.append(dt_utc_aware)
    print(prices_series_24h[-1]-prices_series_24h[0])
    logger.info("get api")
    return {"time_series_24h":time_series_24h,"prices_series_24h":prices_series_24h,"chanhePrice_24h":prices_series_24h[-1]-prices_series_24h[0]}

@router.get("/crypto/top250_market_now",tags=["crypto"])
async def get_coinlist_top250_market_now():
    url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1&sparkline=true&price_change_percentage=1h%2C24h%2C7d"
    data=requests.get(url)

    return data.json()

@router.get("/crypto/market_now/{coinlist}",tags=["crypto"])
async def get_coinlist_market_now(coinlist):
    url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={coinlist}&order=market_cap_desc&per_page=100&page=1&sparkline=true&price_change_percentage=1h,24h,7d"
    market_list=requests.get(url)
    for coin in market_list.json():
        pass
    return "ok"

@router.get("/crypto/top250_market_symbol",tags=["crypto"])
async def get_coinlist_top250_market_now():
    url=f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=250&page=1"
    data=requests.get(url)
    symbol_list=[]
    for item in data.json():
        res = dict((k, item[k]) for k in ['symbol', 'id','name'] if k in item)
        symbol_list.append(res)
    return {"symbol":symbol_list}