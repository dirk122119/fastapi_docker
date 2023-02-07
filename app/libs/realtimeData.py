import requests
import pandas as pd
from dotenv import load_dotenv
import os
from loguru import logger
import redis
import time
import json
from redis.commands.json.path import Path
from dotenv import load_dotenv
import os


def yahoo_realtime_data():
    target_dic={"tw_index":"^TWII",
    "0050":"0050.TW",
    "0051":"0051.TW",
    "Dow Jones Industrial Average":"^DJI",
    "S&P 500":"^GSPC",
    "NASDAQ Composite":"^IXIC",
    "BTC/USDT":"BTC-USD",
    "ETH/USDT":"ETH-USD",
    "BNB/USDT":"BNB-USD"}

    realtime_dic={}
    for key,value in target_dic.items():
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{value}?region=US&lang=en-US&includePrePost=false&interval=2m&useYfid=true&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance"
        payload={}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
        response = requests.request("GET", url, headers=headers, data=payload)
        if (response.json()["chart"]["result"]):
            data={
                "symbol":response.json()["chart"]["result"][0]["meta"]["symbol"],
                "last_time":response.json()["chart"]["result"][0]["meta"]["regularMarketTime"],
                "timezone":response.json()["chart"]["result"][0]["meta"]["timezone"],
                "latest_price":response.json()["chart"]["result"][0]["meta"]["regularMarketPrice"],
                "previouse_close_price":response.json()["chart"]["result"][0]["meta"]["chartPreviousClose"],
                "dataGranularity":response.json()["chart"]["result"][0]["meta"]["dataGranularity"],
                "range":response.json()["chart"]["result"][0]["meta"]["range"],
                "timestamp":response.json()["chart"]["result"][0]["timestamp"],
                "price_high":response.json()["chart"]["result"][0]["indicators"]["quote"][0]["high"],
                "price_close":response.json()["chart"]["result"][0]["indicators"]["quote"][0]["close"],
                "price_low":response.json()["chart"]["result"][0]["indicators"]["quote"][0]["low"],
                "price_open":response.json()["chart"]["result"][0]["indicators"]["quote"][0]["open"],
                "price_volume":response.json()["chart"]["result"][0]["indicators"]["quote"][0]["volume"],}
        else:
            data={
                "code":response.json()["chart"]["error"]["code"],
                "description":response.json()["chart"]["error"]["description"]
            }
        realtime_dic[key]=data
    load_dotenv()
    client = redis.Redis(host=os.getenv('Redis_host'), port=os.getenv('Redis_port'),password=os.getenv('Redis_password'))
    client.json().set('realtime:data', Path.root_path(), realtime_dic)

def get_dashboard_data():
    target_dic={"tw_index":"^TWII",
    "0050":"0050.TW",
    "0051":"0051.TW",
    "Dow Jones Industrial Average":"^DJI",
    "S&P 500":"^GSPC",
    "NASDAQ Composite":"^IXIC",
    "BTC/USDT":"BTC-USD",
    "ETH/USDT":"ETH-USD",
    "BNB/USDT":"BNB-USD"}
    symbol_str=""
    for key,value in target_dic.items():
        symbol_str+=f"{value},"
        
    print(symbol_str[0:-1])

    url_quote = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
    querystring_quote = {"region":"US","symbols":symbol_str[0:-1]}
    headers = {
	    "X-RapidAPI-Key": "9662692fbfmsh198d40754c15840p1411c3jsn2113b55048e9",
	    "X-RapidAPI-Host": "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }
    response_quote = requests.request("GET", url_quote, headers=headers, params=querystring_quote)

    realtime_dict={}
    for key,value in target_dic.items():
        index = list(target_dic.values()).index(value)
        response_quote.json()["quoteResponse"]["result"][index]
        res={
            "target":key,
            "currency":response_quote.json()["quoteResponse"]["result"][index]["currency"],
            "last_time":response_quote.json()["quoteResponse"]["result"][index]["regularMarketTime"],
            "last_price":response_quote.json()["quoteResponse"]["result"][index]["regularMarketPrice"],
            "daily_high":response_quote.json()["quoteResponse"]["result"][index]["regularMarketDayHigh"],
            "daily_low":response_quote.json()["quoteResponse"]["result"][index]["regularMarketDayLow"],
            "daily_open":response_quote.json()["quoteResponse"]["result"][index]["regularMarketOpen"],
            "previous_close":response_quote.json()["quoteResponse"]["result"][index]["regularMarketPreviousClose"],

            }
        realtime_dict[value]=res
    

if __name__ == '__main__':
    yahoo_realtime_data()