from fastapi import FastAPI
from pydantic import BaseModel
from loguru import logger
from poi_server.store_address_info import store_address_info_to_redis
from poi_server.poi_search_v2 import poi_v2_around_search
from weather_server.weather_info import get_weather_info_formated

app = FastAPI()

# 定义请求模型
class POIRequest(BaseModel):
    user_name: str
    location: str
    keywords: str = None    # 默认不使用
    
class WeatherRequest(BaseModel):
    location: str
    forecast: bool = True    # 默认查询天气预报

# 根目录访问的处理
@app.get("/")
async def read_root():
    # 0：操作成功（最常见的方式，表示无错误）。1：服务器内部错误。
    return {"code": 0, "msg": "欢迎访问自定义高德开放平台", "data": None}

@app.post("/search_weather/")
async def search_weather(request: WeatherRequest):
    """
    FastAPI 接口：根据用户传入的位置查询天气信息
    """
    # 调用天气查询接口，格式化输出天气信息
    weather_info_formated = await get_weather_info_formated(request.location, request.forecast)
    if weather_info_formated:
        return {"code": "0", "msg": "查询天气成功", "data": weather_info_formated}
    else:
        return {"code": "1", "msg": "查询天气失败", "data": None}

@app.post("/search_poi/")
async def search_poi(request: POIRequest):
    """
    FastAPI 接口：根据用户传入的位置和关键字(默认不使用)搜索附近的兴趣点
    """
    result = await poi_v2_around_search(request.location, request.keywords)
    if result:
        return {"code": "0", "msg": "查询POI成功", "data": result}
    else:
        return {"code": "1", "msg": "查询POI失败", "data": None}


@app.post("/create_gaode_info/")
async def create_gaode_info(request: POIRequest):
    """
    FastAPI 接口：将用户位置、POI信息和用户名存入redis，构建高德地图信息，用于后续查询。
    示例：
    location = "116.482145,39.990039"  # 北京市朝阳区望京街道方恒购物中心方恒国际
    location = "116.468318,40.012600"  # 北京市朝阳区东湖街道叶青大厦C座
    """
    # 调用高德地图API搜索附近的POI
    pois = await poi_v2_around_search(request.location, request.keywords)
    if not pois:
        return {"code": "1", "msg": "查询POI失败", "data": None}
    # 将用户位置、POI信息和用户名存入redis
    await store_address_info_to_redis(request.location, pois, request.user_name)
    # 返回成功信息，因为是存入redis，不需要返回数据
    return {"code": "0", "msg": "POIS及地理信息录入成功", "data": None}

if __name__ == "__main__":
    import uvicorn
    try:
        # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
        uvicorn.run(app, host="0.0.0.0", port=8000)
    except Exception as e:
        logger.error(f"启动服务器时出错: {e}")
