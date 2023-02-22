from fastapi import APIRouter,Cookie,Request,Response
from pydantic import BaseModel
from datetime import datetime
from  app.libs.rdsFunction import create_connection_pool
import mysql.connector
from fastapi.responses import JSONResponse
import json
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
from datetime import datetime,timedelta
import os

private_key=os.getenv('jwtKey')
class Register_User(BaseModel):
    account: str
    email: str
    password:str
    check_password: str 

class Login_User(BaseModel):
    email: str
    password:str

router=APIRouter()
@router.post("/regist",tags=["user"])
async def regist(user: Register_User):
    try:
        cnx=create_connection_pool()
    except:
        return JSONResponse(status_code=400, content={"data":{"message": "無法建立連線"}})
    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    try:
        sql="SELECT * from UserTable where email=%s;"
        value=(user.email,)
        cursor.execute(sql,value)
        result=cursor.fetchone()
        if(result!=None):
            return JSONResponse(status_code=400, content={"data":{"message": "重複的email"}})
        else:
            passwordHashed=generate_password_hash(password=user.password)
            sql="INSERT INTO UserTable (name,account,email,password) value(%s,%s,%s,%s)"
            value=(user.account,user.account,user.email,passwordHashed)
            cursor.execute(sql,value)
            connect_objt.commit()
            response=JSONResponse(status_code=200, content={"data":{"message": "註冊完成"}})
    except mysql.connector.Error as e:
        response=JSONResponse(status_code=400, content={"data":{"message": e.msg}})
    finally:
        cursor.close()
        connect_objt.close()
    return response

@router.put("/login",tags=["user"])
async def login(user: Login_User,res: Response):
    try:
        cnx=create_connection_pool()
    except:
        return JSONResponse(status_code=400, content={"data":{"message": "無法建立連線"}})
    if not(user.email) or not(user.password):
        return JSONResponse(status_code=400, content={"data":{"message": "帳號和密碼不能空白"}})

    connect_objt=cnx.get_connection()
    cursor = connect_objt.cursor()
    try:
        sql="SELECT account,email,password,id from UserTable where email=%s ;"
        value=(user.email,)
        cursor.execute(sql,value)
        result=cursor.fetchone()
        if(result!=None):
            if(check_password_hash(result[2],user.password)):
                expTime=datetime.now()+timedelta(days=7)
                encoded = jwt.encode({"account":result[0],"email": result[1]}, private_key, algorithm="HS256")
                response=JSONResponse(status_code=200, content={"data":{"account":result[0],"message":"login"}})
                response.set_cookie(key="fastJwt", value=encoded,expires=expTime)
            else:
                response=JSONResponse(status_code=400, content={"data":{"message": "信箱或密碼錯誤"}})
        else:
             response=JSONResponse(status_code=400, content={"data":{"message": "無此信箱"}})
    except mysql.connector.Error as e:
        response=JSONResponse(status_code=400, content={"data":{"message": e.msg}})
    finally:
        cursor.close()
        connect_objt.close()
    return response

@router.get("/checkjwt",tags=["user"])
def checkjwt(request: Request):
    token=request.cookies.get('fastJwt')
    print(request.cookies)
    print(token)
    if(token):
        try:
            cnx=create_connection_pool()
        except:
            return JSONResponse(status_code=400, content={"data":{"message": "無法建立連線"}})
        try:
            tokenDecode=jwt.decode(token,private_key,algorithms="HS256")
            connect_objt=cnx.get_connection()
            cursor = connect_objt.cursor()
            sql="SELECT account,email,password from UserTable where email=%s ;"
            value=(tokenDecode["email"],)
            cursor.execute(sql,value)
            result=cursor.fetchone()
            if(result!=None):
                response=JSONResponse(status_code=200, content={"data":{"account":result[0],"email":result[1]}})
            else:
                response=JSONResponse(status_code=400, content={"data":None})
        except mysql.connector.Error as e:
            response=JSONResponse(status_code=400, content={"data":{"message": e.msg}})
        finally:
            cursor.close()
            connect_objt.close()
    else:
        response=JSONResponse(status_code=400, content={"data":None})
    return response