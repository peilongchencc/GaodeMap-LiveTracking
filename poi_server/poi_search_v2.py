"""
Description: 使用高德地图 POI 2.0周边搜索 API 获取附近的兴趣点（异步实现）。
Notes: 目前，高德地图 POI (常规版和2.0)周边搜索 API 的服务端不支持一次性将所有分页数据返回。如果需要获取所有数据，需要多次请求并合并数据。
Difference: 与高德地图 POI 常规版相比，POI 2.0 版本的周边搜索区别只在于返回的数据更干净，可以自定义一些返回字段。
"""
import os
import json
import aiohttp
import asyncio
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")
from poi_server.transfer_format import transform_poi_data

async def poi_v2_around_search(location, keywords=None):
    """
    使用高德地图 POI 2.0周边搜索 API 获取附近的兴趣点（异步实现）。
    
    Args:
        location (str): 中心点经纬度，格式为 "经度,纬度"，例如 "116.481488,39.990464"。
        keywords (str, optional): 查询的关键字，例如 "超市"、"餐厅"。注意：该参数只支持一个关键字。
    Returns:
        dict or None: 返回 POI 搜索结果的 JSON 数据，如果失败则返回 None。
    Notes:
        高德不支持一次性将所有分页数据返回，如果需要获取所有数据，需要多次请求并合并数据。
    Docs:
        高德Web服务API 搜索POI 2.0 https://lbs.amap.com/api/webservice/guide/api-advanced/newpoisearch#t4
        POI分类编码: https://lbs.amap.com/api/webservice/download
    """
    url = "https://restapi.amap.com/v5/place/around"
    params = {
        "location": location,
        "types": "商场|体育休闲服务|风景名胜|餐饮服务|科教文化服务",
        "radius": "5000",
        "sortrule": "weight",
        "output": "json",
        "page": "1",        # 请求的页码
        "page_size": "25",  # 每页的结果数
        "key": os.getenv('GAODE_API_KEY')  # 高德地图 API 的密钥。
    }
    if keywords:
        params["keywords"] = keywords

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # 检查请求状态
                data = await response.json()  # 解析 JSON 数据
                if data.get("status") == "1":  # 判断请求是否成功
                    data_formated = transform_poi_data(data)    # 转换数据格式
                    return data_formated
                else:
                    print(f"请求失败，错误信息：{data.get('info')}")
                    return None
        except aiohttp.ClientError as e:
            print(f"HTTP 请求发生错误：{e}")
            return None

async def main():
    """
    主函数，执行 POI 周边搜索。
    """
    # 示例经纬度和用户 API Key
    location = "116.468318,40.012600"  # 北京市朝阳区东湖街道叶青大厦C座

    result = await poi_v2_around_search(location)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=4))
    
if __name__ == "__main__":
    asyncio.run(main())