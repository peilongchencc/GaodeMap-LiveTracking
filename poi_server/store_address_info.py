"""
存储用户位置信息、POI信息和用户名，构建高德地图信息，用于后续查询。
"""
import json
from loguru import logger
from datetime import datetime
from database.redis_base import RedisManager
from regeo_server.regeo import reverse_geocode, get_formatted_address

# 类似于指定 MySQL 的某个数据库
redis_client = RedisManager.get_redis_client(3)

async def store_address_info_to_redis(location, pois, user_name="中东悍匪"):
    """
    将用户位置、POI信息和用户名存入redis，构建高德地图信息，用于后续查询。
    Args:
        location: str, 用户位置信息
        pois: dict, 附近的POI信息
        user_name: str, 用户名，默认为"中东悍匪"
    Returns:
        None,存入操作，无返回值
    """
    try:
        # 生成当前时间戳
        now = datetime.now()
        timestamp = now.strftime('%Y-%m-%d %H:%M:%S')  # 例如 2025-01-15 14:06:49    
        date_only = now.strftime('%Y%m%d')  # 例如 20250115
        
        # 逆地理编码查询
        re_geocode = await reverse_geocode(location)
        # 获取格式化地址
        formatted_address = get_formatted_address(re_geocode)
        
        # 检查redis中是否存在该键
        key = f"{date_only}-{user_name}"  # 例如 20250115-中东悍匪
        value = await redis_client.get(key)  # 存在返回值，不存在返回None
        
        if value:
            logger.info(f"键名为 {key} 的数据已存在！开始添加新数据")
            data_initialized = json.loads(value)
        else:
            logger.info(f"键名为 {key} 的数据不存在！开始数据初始化！")
            data_initialized = {"collections": []}
        
        data_initialized["collections"].append({
            "timestamp": timestamp,
            "formatted_address": formatted_address,
            "pois": pois
        })
        
        # 数据再度存入redis
        await redis_client.set(key, json.dumps(data_initialized, ensure_ascii=False))  # 确保中文字符正常显示
    except Exception as e:
        logger.error(f"将POIS、地址等高德信息存入Redis时发生错误: {e}")