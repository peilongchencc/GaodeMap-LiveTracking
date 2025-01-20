"""
Description: POI数据依据redis先检查，然后添加数据。再次检查时，追加数据。
Notes: 
"""
import json
import asyncio
from loguru import logger
from datetime import datetime
from database.redis_base import RedisManager

# 类似于指定 MySQL 的某个数据库
redis_client = RedisManager.get_redis_client(3)

pois_1 = {
            "酒吧": ["CLUB禾·高空观景西餐厅"],
            "中餐厅": [
                "望京一号(博雅店)",
                "俄士厨房(北京望京万象汇店)",
                "黄记煌三汁焖锅(望京万象汇店)"
            ],
            "普通商场": ["北京望京万象汇"],
            "上海菜": ["老吉堂上海本帮菜(望京店)"],
            "购物中心": ["望京华彩商业中心"]
                }

pois_2 = {
            "广东菜(粤菜)": ["星粤(望京店)"],
            "商场": ["望京SOHOT1商场", "望京SOHOT2商场"],
            "中餐厅": [
                "潇湘阁(望京SOHO店)",
                "峇峇娘马来西亚餐厅(望京SOHO店)",
                "熊先生柳州螺蛳粉",
                "西粉堂新疆米粉(望京店)",
                "潮黄记·潮汕鲜牛肉火锅(望京店)"
            ],
            "冷饮店": ["CoCo都可(望京SOHOT1商场店)"],
            "科教文化场所": ["G-STEPS街舞工作室(望京SOHO店)"]
                }

pois_3 = {
            "广东菜(粤菜)": ["星粤(望京店)"],
            "商场": ["望京SOHOT1商场", "望京SOHOT2商场"],
            "中餐厅": [
                "潇湘阁(望京SOHO店)",
                "峇峇娘马来西亚餐厅(望京SOHO店)",
                "熊先生柳州螺蛳粉",
                "西粉堂新疆米粉(望京店)",
                "潮黄记·潮汕鲜牛肉火锅(望京店)"
            ],
            "冷饮店": ["CoCo都可(望京SOHOT1商场店)"],
            "科教文化场所": ["G-STEPS街舞工作室(望京SOHO店)"]
                }

async def main():
    # 生成当前时间戳
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    # 例如
    
    date_only = datetime.now().strftime('%Y%m%d')   # 例如 20250115
    user_name = "中东悍匪"
    key = f"{date_only}-{user_name}"    # 例如 20250115-中东悍匪
    
    # 检查键是否存在
    value = await redis_client.get(key)
    if value:
        logger.info(f"键名为 {key} 的数据已存在！开始添加新数据")
        data_initialized = json.loads(value)
        data_initialized["collections"].append({"timestamp": timestamp, "pois": pois_2})
        
        # 数据再度存入redis
        await redis_client.set(key, json.dumps(data_initialized, ensure_ascii=False))  # 确保中文字符正常显示
        logger.info(f"添加后的数据为:")
        value = await redis_client.get(key)
        formatted_value = json.loads(value)
        print(json.dumps(formatted_value, indent=4, ensure_ascii=False))  # 格式化输出
        
    else:
        logger.info(f"键名为 {key} 的数据不存在！开始数据初始化！")
        # 数据初始化
        data_initialization = {"collections": [{"timestamp": timestamp, "pois": pois_1}]}
        # 添加键值对
        await redis_client.set(key, json.dumps(data_initialization, ensure_ascii=False))  # 确保中文字符正常显示
        logger.info(f"初始化的数据为:")
        value = await redis_client.get(key)
        formatted_value = json.loads(value)
        print(json.dumps(formatted_value, indent=4, ensure_ascii=False))  # 格式化输出

async def delete_data():
    # 从 Redis 删除数据
    # 如果指定的键存在且被成功删除，返回值是 1（表示删除了 1 个键）。
    # 如果指定的键不存在，返回值是 0（表示没有键被删除）。
    key = "20250115-中东悍匪"
    result = await redis_client.delete(key)
    print(f"从 Redis 删除数据的result为: {result}")
    if result:
        print(f"键名为 {key} 的数据已删除！")
    else:
        print(f"键名为 {key} 的数据不存在！")

if __name__ == "__main__":
    asyncio.run(main())