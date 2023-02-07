import requests
import pandas as pd
import glob
import time
from loguru import logger

# 檢查存在的檔案
exist_file=[]
files = glob.glob("./stockHistoryData/*.csv")
for table in files:
	exist_file.append(table.split("/")[-1][:-4])

symbols = pd.read_csv("./sp500_qqq_list.csv")
print(symbols["symbol"])

for symbol in symbols["symbol"]:
	if not (symbol in exist_file):
		for index in range(1,6,1):
			try:
				url = "https://alpha-vantage.p.rapidapi.com/query"
				headers = {
					"X-RapidAPI-Key": "9662692fbfmsh198d40754c15840p1411c3jsn2113b55048e9",
					"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
				}

				querystring = {f"function":"TIME_SERIES_DAILY","symbol":{symbol},"outputsize":"full","datatype":"json"}
				response = requests.request("GET", url, headers=headers, params=querystring)

				df= pd.DataFrame(response.json()['Time Series (Daily)'])
				df.T.to_csv(f"./stockHistoryData/{symbol}.csv")
				logger.info(f'{symbol} finish')
				break
			except Exception as e:
				logger.error(f"{symbol} error {index} time,{e}")
				symbol=symbol.replace(".","-")
				time.sleep(300)
			finally:
				time.sleep(10)
print("finish")

