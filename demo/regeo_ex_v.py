"""
Description: 逆地理编码查询示例（异步实现），将经纬度解析成地址。
Notes: 
POI（Point of Interest 兴趣点）通常是某个具体的位置，比如一个餐厅、一座商场。
AOI（Area of Interest 兴趣区域）是更大的区域范围，比如一个小区、一片公园、一块商圈。

逆地理编码接口中的POI数据较少，如果需要更多的POI数据，可以使用周边搜索接口。强行查询自己需要类型的POI数据，例如"体育休闲服务|科教文化服务"，如果没有
会返回默认的"商业住宅"类型的POI数据。
"""
import os
import sys

# 获取当前脚本的绝对路径
current_script_path = os.path.abspath(__file__)
# 获取当前脚本的父目录的父目录
parent_directory_of_the_parent_directory = os.path.dirname(os.path.dirname(current_script_path))
# 将这个目录添加到 sys.path
sys.path.append(parent_directory_of_the_parent_directory)


import aiohttp
import asyncio
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")

async def reverse_geocode(location):
    """
    使用高德地图逆地理编码 API 获取地理信息（异步实现）。

    Args:
        location (str): 经纬度坐标，格式为 "经度,纬度"，例如 "116.481488,39.990464"。
        api_key (str): 高德地图 API 的密钥。

    Returns:
        dict or None: 返回逆地理编码结果的 JSON 数据，如果失败则返回 None。
    """
    url = "https://restapi.amap.com/v3/geocode/regeo"
    params = {
        "location": location,
        "output": "json",  # 返回格式为 JSON
        "extensions": "all",  # 在 extensions 字段值为 all 时才会返回 POI(Point of Interest 兴趣点) 内容
        # "poitype": "商场|体育休闲服务|风景名胜|餐饮服务|中餐厅|科教文化服务",  # 搜索类别，例如 "餐饮服务"、"商务住宅" 等，多个类别用 "|" 分割
        "poitype": "体育休闲服务|科教文化服务",
        "radius": "1500",  # 查询半径，取值范围：0~3000，默认1000，单位：米
        # "roadlevel": "1",  # 道路等级，可选值：0,1，当 roadlevel=1时，过滤非主干道路，仅输出主干道路数据
        "key": os.getenv('GAODE_API_KEY')  # 高德地图 API 的密钥。
    }

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
    主函数，执行逆地理编码查询。
    """
    # 示例经纬度和用户 API Key
    # location = "116.482145,39.990039"  # 北京某位置的经纬度
    location = "116.468318,40.012600"   # 北京市朝阳区东湖街道叶青大厦C座

    result = await reverse_geocode(location)
    if result:
        print("逆地理编码结果：")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())