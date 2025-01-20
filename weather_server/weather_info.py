import os
import aiohttp
import asyncio
from loguru import logger
from dotenv import load_dotenv
# 环境变量必须要在使用环境变量中配置前导入
load_dotenv("env_config/.env.local")
from regeo_server.regeo import reverse_geocode, get_adcode

def get_formatted_weather_live(weather_live):
    """
    格式化实时天气信息。
    
    Args:
        weather_live (dict): 实时天气信息。
    
    Returns:
        str: 格式化后的实时天气信息。
    """
    live = weather_live["lives"][0]
    formatted = (
        f"{live.get('province')}{live.get('city')}\n"
        f"天气：{live.get('weather')}\n"
        f"温度：{live.get('temperature')}°C\n"
        f"风向：{live.get('winddirection')}\n"
        f"风力：{live.get('windpower')}\n"
        f"湿度：{live.get('humidity')}%\n"
        f"数据发布时间：{live.get('reporttime')}"
    )
    return formatted

def get_formatted_weather_forecast(weather_forecast):
    """
    格式化天气预报信息，仅包含今天和明天的数据。
    
    Args:
        weather_forecast (dict): 天气预报信息。
    
    Returns:
        str: 格式化后的天气预报信息。
    """
    forecast = weather_forecast["forecasts"][0]
    formatted = (
        f"{forecast.get('province')}{forecast.get('city')}\n"
        f"数据发布时间：{forecast.get('reporttime')}\n"
    )
    for cast in forecast.get("casts")[:2]:  # 只获取今天和明天的数据
        formatted += (
            f"{cast.get('date')}（星期{cast.get('week')}）\n"
            f"白天天气：{cast.get('dayweather')}\n"
            f"夜晚天气：{cast.get('nightweather')}\n"
            f"白天最高温度：{cast.get('daytemp')}°C\n"
            f"夜晚最低温度：{cast.get('nighttemp')}°C\n"
            f"白天风向：{cast.get('daywind')}\n"
            f"夜晚风向：{cast.get('nightwind')}\n"
            f"白天风力：{cast.get('daypower')}级\n"
            f"夜晚风力：{cast.get('nightpower')}级\n"
        )
    return formatted

async def weather_infomation(adcode, forecast=False):
    """
    使用高德地图天气查询 API 获取天气信息（异步实现）。
    
    Args:
        adcode (str): 行政区划代码（Adcode）。
        forecast (bool): 是否查询天气预报。
            - False: 查询实况天气。
            - True: 查询未来4天的天气预报。
    
    Returns:
        dict or None: 返回天气查询结果的 JSON 数据，如果失败则返回 None。
    """
    url = "https://restapi.amap.com/v3/weather/weatherInfo"
    # 从环境变量中获取高德地图 API 密钥
    api_key = os.getenv('GAODE_API_KEY')
    if not api_key:
        logger.error("API key is not set. Please set the GAODE_API_KEY environment variable.")
        return None
    
    # 根据 forecast 参数决定 extensions 参数的值，实况天气查询为 "base"，天气预报查询为 "all"
    # "all" 查询的是未来4天的天气预报，包括当天、明天、后天和大后天
    extensions = "all" if forecast else "base"
    
    params = {
        "city": adcode,
        "output": "json",  # 返回格式为 JSON
        "extensions": extensions,  # 查询类型
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

async def get_weather_info(location, forecast=False):
    """
    获取实时天气和天气预报信息。
    
    Args:
        location (str): 经纬度信息，格式为 "经度,纬度"。
        forecast (bool): 是否查询天气预报。
            - False: 查询实况天气。
            - True: 查询今天、明天的天气预报。默认是查询今天、明天、后天和大后天的天气预报。
    Returns:
        tuple: 包含实时天气和天气预报信息的元组。
    """
    try:
        # 执行逆地理编码查询
        re_geocode = await reverse_geocode(location)
        # 获取行政区划代码
        adcode = get_adcode(re_geocode)
        # 天气查询
        weather_info = await weather_infomation(adcode, forecast)
        return weather_info
    except Exception as e:
        logger.error(f"获取天气信息时发生错误：{e}")
        return None

async def get_weather_info_formated(location, forecast=False):
    """
    获取格式化的实时天气和天气预报信息。
    
    Args:
        location (str): 经纬度信息，格式为 "经度,纬度"。
        forecast (bool): 是否查询天气预报。
            - False: 查询实况天气。
            - True: 查询今天、明天的天气预报。默认是查询今天、明天、后天和大后天的天气预报。
    Returns:
        str: 格式化后的天气信息。
    """
    # 获取天气信息
    weather_info = await get_weather_info(location, forecast)
    if weather_info:    # 如果查询成功
        if forecast:    # 如果查询天气预报
            formatted = get_formatted_weather_forecast(weather_info)
        else:           # 如果查询实况天气
            formatted = get_formatted_weather_live(weather_info)
        return formatted
    else:               # 如果查询失败
        return None

async def main():
    """
    主函数，执行天气查询。
    """
    # 示例经纬度和用户 API Key
    # location = "116.482145,39.990039"  # 北京某位置的经纬度
    location = "116.468318,40.012600"   # 北京市朝阳区东湖街道叶青大厦C座
    forecast = False  # 是否查询天气预报, False 为查询实况天气, True 为查询天气预报
    weather_info_formated = await get_weather_info_formated(location, forecast)
    if weather_info_formated:
        logger.info(f"天气信息：\n{weather_info_formated}")
    else:
        logger.error("获取天气信息失败")

if __name__ == "__main__":
    asyncio.run(main())