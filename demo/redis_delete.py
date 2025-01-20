"""
Description: 此脚本连接到 Redis 数据库，设置一些键值对，检索一个值，并删除指定的键。
Notes:  `redis_client.delete` 方法接受一个或多个键名作为参数，并返回成功删除的键数量。
Terminal Output:

```txt
键 key_1 的值为: value_1
尝试删除以下键：['key_1', 'key_2', 'key_4']
成功删除的键数量为: 2
```
"""
import redis.asyncio as redis
import asyncio
from redis.exceptions import RedisError

# 创建 Redis 连接，指定密码和数据库索引
redis_client = redis.Redis(
    host="localhost",  # 替换为你的 Redis 地址
    port=6379,         # Redis 端口
    password="123456", # Redis 密码
    db=3,              # 数据库索引
    decode_responses=True  # 使返回值为字符串类型，而不是字节类型
)

async def main():
    try:
        # 添加键值对
        await redis_client.set("key_1", "value_1")
        await redis_client.set("key_2", "value_2")
        await redis_client.set("key_3", "value_3")

        # 查看键值对
        value = await redis_client.get("key_1")
        print(f"键 key_1 的值为: {value}")

        # 删除键值对
        keys_to_delete = ["key_1", "key_2", "key_4"]
        deleted_count = await redis_client.delete(*keys_to_delete)
        print(f"尝试删除以下键：{keys_to_delete}")
        print(f"成功删除的键数量为: {deleted_count}")
    except RedisError as e:
        print(f"Redis 错误: {e}")
    finally:
        # 关闭连接
        await redis_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())