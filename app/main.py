from fastapi import FastAPI,Request
import uvicorn
from app.routers import crypto,upload,us_stock,tw_stock
from app.page import home
from app.routers import redis
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from redis import asyncio as aioredis
from dotenv import load_dotenv
import os

async def connect_redis():
    load_dotenv()
    redis = await aioredis.from_url(f"redis://{os.getenv('Redis_host')}:{os.getenv('Redis_port')}",password=os.getenv('Redis_password'))
    return redis

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/app/static", StaticFiles(directory="app/static"), name="static")
app.include_router(crypto.router)
app.include_router(us_stock.router)
app.include_router(tw_stock.router)
app.include_router(upload.router)
app.include_router(redis.router)
app.include_router(home.router)
templates = Jinja2Templates(directory="templates/")


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.on_event("startup")
async def create_redis():
    app.state.redis = await connect_redis()


@app.on_event("shutdown")
async def close_redis():
    await app.state.redis.close()

if __name__=='__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
