from fastapi import FastAPI
from pydantic import BaseModel
from poi_server.poi_search_v2 import poi_v2_around_search

app = FastAPI()

# 定义请求模型
class POIRequest(BaseModel):
    location: str
    keywords: str = None    # 默认不使用

@app.post("/search_poi/")
async def search_poi(request: POIRequest):
    """
    FastAPI 接口：根据用户传入的位置和关键字(默认不使用)搜索附近的兴趣点
    """
    result = await poi_v2_around_search(request.location, request.keywords)
    return result
