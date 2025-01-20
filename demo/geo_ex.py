"""
Description: 地理编码查询示例（异步实现），地址解析成经纬度坐标。
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


import aiohttp
import asyncio
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")

async def geocode(address):
    """
    使用高德地图地理编码 API 获取地理信息（异步实现）。

    Args:
        address (str): 需要查询的地址，例如 "北京市朝阳区阜通东大街6号"。

    Returns:
        dict or None: 返回地理编码结果的 JSON 数据，如果失败则返回 None。
    """
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": address,
        "output": "json",  # 返回格式为 JSON
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
    主函数，执行地理编码查询。
    """
    address = "北京市朝阳区阜通东大街6号"
    # address = "北京市朝阳区东湖街道叶青大厦C座"
    # address = "北京市朝阳区望京街10号"

    result = await geocode(address)
    if result:
        print("地理编码结果：")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())