from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from  app.libs.rdsFunction import create_connection_pool
import mysql.connector
from fastapi.responses import JSONResponse
import json

class Game(BaseModel):
    market: str
    symbol: str
    date: datetime
    target: float 
    direction:str
    createrEmail:str

router=APIRouter()
@router.post("/create_game/",tags=["game"])
async def create_game(game: Game):
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    try:
        sql="select id from UserTable where email=%s"
        value=(game.createrEmail,)
        cursor.execute(sql,value)
        result=cursor.fetchone()
        if(result!=None):
            sql="INSERT INTO GameTable (market,symbol,date,price,direct,createrId) value(%s,%s,%s,%s,%s,%s)"
            value=(game.market,game.symbol,game.date.date(),float(game.target),game.direction,result[0])
            cursor.execute(sql,value)
            connect_objt.commit()
            response=JSONResponse(status_code=200, content={"message": "create finish"})
        else:
             response=JSONResponse(status_code=400, content={"data":{"message": "無此信箱"}})
        
    except mysql.connector.Error as e:
        response=JSONResponse(status_code=400, content={"message": e.msg})
    finally:
        cursor.close()
        connect_objt.close()
    return response

@router.get("/get_game/",tags=["game"])
async def get_game():
    try:
        cnx=create_connection_pool()
    except:
        print("無法建立connect pool")

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    sql="select market,symbol,date,price,direct,createrId from GameTable;"
    cursor.execute(sql)
    data=cursor.fetchall()
    data_list=[]
    for row in data:
        sql="select name from UserTable where id=%s;"
        value=(row[5],)
        cursor.execute(sql,value)
        user=cursor.fetchone()
        data_list.append({"market":row[0],"symbol":row[1],"date":str(row[2]),"price":row[3],"direct":row[4],"creater":user[0]})
    return JSONResponse(status_code=200, content={"data":data_list})