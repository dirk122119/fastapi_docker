from fastapi import APIRouter,Request

router=APIRouter()
@router.get("/redis_dashboard", tags=["redis"])
async def redis_get_dashboard(request:Request):
    value= await request.app.state.redis.json().get("realtime:dashboard")
    return value

@router.get("/redis_tw", tags=["redis"])
async def redis_get_tw_realtime(request:Request):
    value= await request.app.state.redis.json().get("realtime:TW_realtime")
    return value

@router.get("/redis_us", tags=["redis"])
async def redis_get_us_daily(request:Request):
    value= await request.app.state.redis.json().get("realtime:US_daily")
    return value

@router.get("/redis_crypto", tags=["redis"])
async def redis_crypto_realtime(request:Request):
    value= await request.app.state.redis.json().get("realtime:crypto")
    return value

@router.get("/redis_coingecko_top7", tags=["redis"])
async def redis_crypto_coingecko_top7(request:Request):
    value= await request.app.state.redis.json().get("realtime:crypto_top7")
    return value

@router.get("/redis_crypto_symbol", tags=["redis"])
async def redis_crypto_realtime(request:Request):
    value= await request.app.state.redis.json().get("realtime:crypto_symbol")
    return value