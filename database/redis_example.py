"""
Description: POI数据依据redis存储测试。
Notes: 
"""
from redis_base import RedisManager
import asyncio
import json

# 类似于指定 MySQL 的某个数据库
redis_client = RedisManager.get_redis_client(3)

async def main():
    # 示例 JSON 数据
    json_data = {
        "中东悍匪": {
            "user_id": 1001,
            "collections": [
                {
                    "timestamp": "2025-01-14 10:30:29",
                    "pois": {
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
                },
                {
                    "timestamp": "2025-01-14 12:30:29",
                    "pois": {
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
                }
            ]
        }
    }
    # 存储数据到 Redis
    key = "user:中东悍匪"
    await redis_client.set(key, json.dumps(json_data["中东悍匪"]))
    print(f"数据已存储到 Redis，键名为: {key}")

    # 从 Redis 检索数据
    retrieved_data = await redis_client.get(key)
    if retrieved_data:
        retrieved_data = json.loads(retrieved_data)
        print("从 Redis 检索到的数据:", type(retrieved_data))
        json_dumps_data = json.dumps(retrieved_data, indent=4, ensure_ascii=False)
        print(json_dumps_data)
        print("数据类型:", type(json_dumps_data))
    else:
        print("未找到对应数据！")

    # 从 Redis 删除数据
    # 如果指定的键存在且被成功删除，返回值是 1（表示删除了 1 个键）。
    # 如果指定的键不存在，返回值是 0（表示没有键被删除）。
    result = await redis_client.delete(key)
    print(f"从 Redis 删除数据的result为: {result}")
    if result:
        print(f"键名为 {key} 的数据已删除！")
    else:
        print(f"键名为 {key} 的数据不存在！")

if __name__ == "__main__":
    asyncio.run(main())