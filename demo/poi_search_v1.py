"""
Description: 使用高德地图 POI (常规版)周边搜索 API 获取附近的兴趣点（异步实现）。
Notes: 
"""
import os
import sys

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 获取当前脚本的父目录的父目录
parent_directory_of_the_parent_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(parent_directory_of_the_parent_directory)

import json
import aiohttp
import asyncio
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")

async def poi_v1_around_search(location, keywords=None):
    """
    使用高德地图 POI 周边搜索 API 获取附近的兴趣点（异步实现）。

    Args:
        location (str): 中心点经纬度，格式为 "经度,纬度"，例如 "116.481488,39.990464"。
        api_key (str): 高德地图 API 的密钥。
        keywords (str, optional): 查询的关键字，例如 "超市"、"餐厅"。注意：该参数只支持一个关键字。

    Returns:
        dict or None: 返回 POI 搜索结果的 JSON 数据，如果失败则返回 None。
    """
    url = "https://restapi.amap.com/v3/place/around"
    params = {
        "location": location,
        "types": "商场|体育休闲服务|风景名胜|餐饮服务|科教文化服务",
        "radius": "5000",
        "sortrule": "weight",
        "output": "json",
        "page": "1",
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
                    return data
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
    # keywords = "餐厅"  # 查询关键字，例如“餐厅”

    result = await poi_v1_around_search(location)
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=4))
    
if __name__ == "__main__":
    asyncio.run(main())