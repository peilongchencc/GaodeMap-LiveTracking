"""
Description: 逆地理编码查询示例（异步实现），将经纬度解析成地址。
Notes: 
"""
import os
import aiohttp
import asyncio
from loguru import logger
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")

def get_formatted_address(data):
    """
    从逆地理编码结果中提取格式化地址。

    Args:
        data (dict): 逆地理编码结果的 JSON 数据。

    Returns:
        str: 格式化地址字符串。
    """
    return data.get("regeocode").get("formatted_address")

def get_adcode(data):
    """
    从逆地理编码结果中提取行政区划代码（Adcode）。

    Args:
        data (dict): 逆地理编码结果的 JSON 数据。

    Returns:
        str: 行政区划代码字符串。
    """
    return data.get("regeocode").get("addressComponent").get("adcode")

async def reverse_geocode(location):
    """
    使用高德地图逆地理编码 API 获取地理信息（异步实现）。

    Args:
        location (str): 经纬度坐标，格式为 "经度,纬度"，例如 "116.481488,39.990464"。

    Returns:
        dict or None: 返回逆地理编码结果的 JSON 数据，如果失败则返回 None。
    """
    url = "https://restapi.amap.com/v3/geocode/regeo"
    # 从环境变量中获取高德地图 API 密钥
    api_key = os.getenv('GAODE_API_KEY')
    if not api_key:
        logger.error("API key is not set. Please set the GAODE_API_KEY environment variable.")
        return None
    
    params = {
        "location": location,
        "output": "json",  # 返回格式为 JSON
        "key": api_key
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # 检查请求状态
                data = await response.json()  # 解析 JSON 数据
                if data.get("status") == "1":  # 判断请求是否成功
                    return data
                else:
                    logger.error(f"请求失败，错误信息：{data.get('info')}")
                    return None
        except aiohttp.ClientError as e:
            logger.error(f"HTTP 请求发生错误：{e}")
            return None

async def main():
    """
    主函数，执行逆地理编码查询。
    Outputs:
    逆地理编码结果：
        {'status': '1', 'regeocode': {'addressComponent': {'city': [], 'province': '北京市', 'adcode': '110105', 'district': '朝阳区', 'towncode': '110105043000', 'streetNumber': {'number': '11号', 'location': '116.468288,40.012327', 'direction': '南', 'distance': '30.5019', 'street': '望京北路'}, 'country': '中国', 'township': '东湖街道', 'businessAreas': [{'location': '116.453779,40.034234', 'name': '来广营', 'id': '110105'}, {'location': '116.470293,39.996171', 'name': '望京', 'id': '110105'}], 'building': {'name': '叶青大厦C座', 'type': '商务住宅;楼宇;商务写字楼'}, 'neighborhood': {'name': [], 'type': []}, 'citycode': '010'}, 'formatted_address': '北京市朝阳区东湖街道叶青大厦C座'}, 'info': 'OK', 'infocode': '10000'}
        **************************************************
        格式化地址： 北京市朝阳区东湖街道叶青大厦C座
        行政区划代码： 110105
    """
    # 示例经纬度和用户 API Key
    # location = "116.482145,39.990039"  # 北京某位置的经纬度
    location = "116.468318,40.012600"   # 北京市朝阳区东湖街道叶青大厦C座
    
    # 执行逆地理编码查询
    result = await reverse_geocode(location)
    if result:
        print("逆地理编码结果：")
        print(result)
        print("*" * 50)
        print("格式化地址：", get_formatted_address(result))
        print("行政区划代码：", get_adcode(result))

if __name__ == "__main__":
    asyncio.run(main())