"""
Description: 尝试删除 Redis 中的单个键。
Notes: `redis_client.delete` 方法接受一个或多个键名作为参数，并返回成功删除的键数量。获取键时，如果键不存在，则返回 None。
Terminal Output:

```txt
键 key_3 的值为: value_3
尝试删除以下键：['key_3']
成功删除的键数量为: 1
键 key_3 的值为: None
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
        # 查看键值对
        value = await redis_client.get("key_3")
        print(f"键 key_3 的值为: {value}")

        # 删除键值对
        keys_to_delete = ["key_3"]
        deleted_count = await redis_client.delete(*keys_to_delete)
        print(f"尝试删除以下键：{keys_to_delete}")
        print(f"成功删除的键数量为: {deleted_count}")
        
        # 查看键值对
        value = await redis_client.get("key_3")
        print(f"键 key_3 的值为: {value}")
    except RedisError as e:
        print(f"Redis 错误: {e}")
    finally:
        # 关闭连接
        await redis_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())