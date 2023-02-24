from fastapi import APIRouter,Request

router=APIRouter()
@router.get("/redis", tags=["redis"])
async def redis_index(request:Request):
    value= await request.app.state.redis.json().get("realtime:dashboard")
    return value

@router.get("/redis_tw", tags=["redis"])
async def redis_index(request:Request):
    value= await request.app.state.redis.json().get("realtime:tw")
    return value
