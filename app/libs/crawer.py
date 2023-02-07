from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
symbol_list=[]
company_name_list=[]

def get_sp500_list(symbol_list,company_name_list):
    url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks'
    browser.get(url)
    rows = browser.find_elements(By.XPATH,"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr")

    print(len(rows))
    for i in range (1, len(rows) + 1) :
        symbol = browser.find_element(By.XPATH,f"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[{i}]/td[1]").text
        if not (symbol in symbol_list):
            company_name = browser.find_element(By.XPATH,f"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[{i}]/td[2]").text
            symbol_list.append(symbol)
            company_name_list.append(company_name)
    return [symbol_list,company_name_list]
    # df = pd.DataFrame({'symbol':symbol_list,'name':company_name_list})
    # df.to_csv("sp500_list.csv",index=False)

def get_qqq_list(symbol_list,company_name_list):
    url='https://en.wikipedia.org/wiki/Nasdaq-100'
    browser.get(url)
    rows = browser.find_elements(By.XPATH,"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[5]/tbody/tr")

    print( len(rows))
    for i in range (1, len(rows) + 1) :
        symbol = browser.find_element(By.XPATH,f"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[5]/tbody/tr[{i}]/td[2]").text
        company_name = browser.find_element(By.XPATH,f"/html/body/div[1]/div/div[3]/main/div[2]/div[3]/div[1]/table[5]/tbody/tr[{i}]/td[1]").text
            
        symbol_list.append(symbol)
        company_name_list.append(company_name)
        # print(f"{symbol} {company_name}")
    return [symbol_list,company_name_list]
def get_0050_list(symbol_list,company_name_list):
    url='https://www.yuantaetfs.com/product/detail/0050/ratio'
    browser.get(url)
    btn = browser.find_element(By.CLASS_NAME, 'moreBtn')
    btn.click()
    rows = browser.find_elements(By.XPATH, 'html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div')
    
    for i in range (1, len(rows)+1) :
        symbol = browser.find_element(By.XPATH,f"/html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[{i}]/div[1]/span[2]").text
        company_name = browser.find_element(By.XPATH,f"/html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[{i}]/div[2]/span[2]").text
        print(f"NO.{i} get {symbol} and {company_name}")
        symbol_list.append(symbol)
        company_name_list.append(company_name)

    return [symbol_list,company_name_list]

def get_0051_list(symbol_list,company_name_list):
    url='https://www.yuantaetfs.com/product/detail/0051/ratio'
    browser.get(url)
    btn = browser.find_element(By.CLASS_NAME, 'moreBtn')
    btn.click()
    rows = browser.find_elements(By.XPATH, '/html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div')
    print(len(rows))
    for i in range (1, len(rows)+1) :
        symbol = browser.find_element(By.XPATH,f"/html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[{i}]/div[1]/span[2]").text
        company_name = browser.find_element(By.XPATH,f"/html/body/div/div/div/section/div/div/div[2]/div[3]/div/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[{i}]/div[2]/span[2]").text
        print(f"NO.{i} get {symbol} and {company_name}")
        symbol_list.append(symbol)
        company_name_list.append(company_name)

    return [symbol_list,company_name_list]

def us_symbol_to_csv():
    symbol_list=[]
    company_name_list=[]
    qqq_list=get_qqq_list(symbol_list,company_name_list)
    symbol_list=qqq_list[0]
    company_name_list=qqq_list[1]
    sp500_list=get_sp500_list(symbol_list,company_name_list)

    df = pd.DataFrame({'symbol':sp500_list[0],'name':sp500_list[1]})
    df.to_csv("sp500_qqq_list.csv",index=False)

def tw_symbol_to_csv():
    symbol_list=[]
    company_name_list=[]
    tw_0050_0051_list=get_0050_list(symbol_list,company_name_list)
    tw_0050_0051_list=get_0051_list(tw_0050_0051_list[0],tw_0050_0051_list[1])
    df = pd.DataFrame({'symbol':tw_0050_0051_list[0],'name':tw_0050_0051_list[1]})
    df.to_csv("tw_0050_0051_list.csv",index=False)

# tw_symbol_to_csv()
tw_symbol_to_csv()
