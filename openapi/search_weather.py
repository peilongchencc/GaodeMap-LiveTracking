import aiohttp
import asyncio

async def query_weather(location, forecast=True):
    """
    异步调用 search_weather 接口查询天气信息。
    Args:
        location (str): 查询的位置信息 (如: 城市名称或经纬度)。
        forecast (bool): 是否查询天气预报，默认为 True。
    Returns:
        dict: 接口返回的数据，如果请求失败或异常则返回 None。
    """
    url = "http://47.95.198.215:8000/search_weather/"   # 如果是访问本地接口，使用 "localhost" 。
    payload = {
        "location": location,
        "forecast": forecast
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    result = await response.json()
                    return result
                else:
                    print(f"请求失败，状态码: {response.status}")
                    return None
        except Exception as e:
            print(f"请求异常: {e}")
            return None

async def main():
    # 查询经纬度对应的天气信息
    location = "116.482145,39.990039"
    forecast = True # 查询天气预报
    result = await query_weather(location, forecast)
    
    if result:
        print(type(result)) # <class 'dict'>
        if result["code"] == "0":
            print("查询天气成功:")
            print(result["data"])
        else:
            print(f"查询失败: {result['msg']}")
    else:
        print("未能获取天气信息。")

if __name__ == "__main__":
    asyncio.run(main())