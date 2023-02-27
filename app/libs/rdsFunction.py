import json 
import mysql.connector
from dotenv import load_dotenv,dotenv_values
import os
import glob
import pandas as pd

def create_connection_pool():
    # change db_config on EC2
    load_dotenv()
    db_config = {
        'host' : os.getenv('sqlHost'),
        'user' : os.getenv('sqlUser'),
        'password' : os.getenv('sqlPassword'),
        'database' : os.getenv('sqlDatabase'),
        'port' : os.getenv('sqlPort')
    }
    cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name = "rds",pool_size=10, **db_config)
    return cnxpool

def createUsSymbolsTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="create table UsSymbols( id int auto_increment Primary KEY, symbol varchar(255) not null, companyName varchar(255) not null);"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()


def createUsStockTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql=f"create table UsStockTable(id int auto_increment Primary KEY,symbol int not null,date DATE not null, open float not null,high float not null,low float not null,close float not null,volume float not null,FOREIGN KEY (symbol) REFERENCES UsSymbols(id));"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()

def stockPriceInOnetabel(cnx):  
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()

    files = glob.glob('./stockHistoryData/*.csv')
    for file in files:
        symbol=file.split("/")[-1][:-4]

        sql="select id from UsSymbols WHERE symbol = %s"
        val=(symbol,)
        cursor.execute(sql,val)
        symbolId=cursor.fetchone()

        df = pd.read_csv(file)
        for i in range (0,df.shape[0]):
            sql=f"INSERT INTO UsStockTable(symbol,date,open,high,low,close,volume) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            val=(symbolId[0],pd.to_datetime(df.iloc[i]["Unnamed: 0"]).strftime('%Y-%m-%d'),df.iloc[i]["1. open"].item(),df.iloc[i]["2. high"].item(),df.iloc[i]["3. low"].item(),df.iloc[i]["4. close"].item(),df.iloc[i]["5. volume"].item())
            cursor.execute(sql,val)
            connect_objt.commit()
    cursor.close()
    connect_objt.close()



def UsSymbo_to_RDS(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    df = pd.read_csv("./us_symbol_list.csv")
    for i in range (0,df.shape[0]):
        sql="INSERT INTO UsSymbols (symbol,companyName) VALUES(%s,%s)"
        val=(df.iloc[i]["stock_id"],df.iloc[i]["stock_name"])
        cursor.execute(sql,val)
        connect_objt.commit()
    cursor.close()
    connect_objt.close()


def createTwSymbolsTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="create table TwSymbols( id int auto_increment Primary KEY, symbol varchar(255) not null, companyName varchar(255) not null);"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()

def createTwStockTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql=f"create table TwStockTable(id int auto_increment Primary KEY,symbol int not null,date DATE not null, open float not null,high float not null,low float not null,close float not null,volume float not null,FOREIGN KEY (symbol) REFERENCES TwSymbols(id));"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()

def TwSymbo_to_RDS(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    df = pd.read_csv("./tw_symbol_list.csv")
    for i in range (0,df.shape[0]):
        sql="INSERT INTO TwSymbols (symbol,companyName) VALUES(%s,%s)"
        val=(df.iloc[i]["stock_id"],df.iloc[i]["stock_name"])
        cursor.execute(sql,val)
        connect_objt.commit()
    cursor.close()
    connect_objt.close()

def createGameTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="create table GameTable(id int auto_increment Primary KEY,market varchar(255) not null,symbol varchar(255) not null,date DATE not null,price float not null ,direct varchar(255) not null,createrId int not null)"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()

def createUserTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="create table UserTable(id int auto_increment Primary KEY,name varchar(255) not null,account varchar(255) not null,password varchar(255) not null,email varchar(255) not null,UNIQUE (email))"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()

def createParticipateTable(cnx):
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="create table ParticipateTable(id int auto_increment Primary KEY,gameId int not null,userId int not null,opinion BOOLEAN not null)"
    cursor.execute(sql,)
    cursor.close()
    connect_objt.close()


load_dotenv()
try:
    cnx=create_connection_pool()
except:
    print("無法建立connect pool")

if __name__ == '__main__':
    TwSymbo_to_RDS(cnx)
    UsSymbo_to_RDS(cnx)