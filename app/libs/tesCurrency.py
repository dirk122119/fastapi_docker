import requests

url = "https://alpha-vantage.p.rapidapi.com/query"
headers = {
	"X-RapidAPI-Key": "9662692fbfmsh198d40754c15840p1411c3jsn2113b55048e9",
	"X-RapidAPI-Host": "alpha-vantage.p.rapidapi.com"
		}
querystring = {f"function":"CRYPTO_INTRADAY","symbols":"ETH,BTC","market":"USD","interval":"5min"}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.json())
