"""
Description: 获取redis中指定用户的高德数据; 从 Redis 删除指定用户的高德数据。
Notes: 
"""
import json
import asyncio
import argparse
from loguru import logger
from datetime import datetime
from database.redis_base import RedisManager

# 类似于指定 MySQL 的某个数据库
redis_client = RedisManager.get_redis_client(3)

async def get_data(user_name):
    """获取redis中指定用户的高德数据。

    Args:
        user_name (str): 用户名。

    Returns:
        None
    """
    date_only = datetime.now().strftime('%Y%m%d')   # 例如 20250115
    key = f"{date_only}-{user_name}"    # 例如 20250115-中东悍匪    
    
    # 检查键是否存在
    value = await redis_client.get(key)
    if value:
        logger.info(f"键名为 {key} 的数据已存在！数据如下：")
        data_initialized = json.loads(value)        
        print(json.dumps(data_initialized, indent=4, ensure_ascii=False))  # 格式化输出
        
    else:
        logger.info(f"键名为 {key} 的数据不存在！")

async def delete_data(user_name):
    """从 Redis 删除指定用户的高德数据。
    Args:
        user_name (str): 用户名。
    Returns:
        None
    Notes:
        使用 Redis 的 delete() 方法删除指定键时，返回值的含义如下：
        如果指定的键存在且被成功删除，返回值是 1（表示删除了 1 个键）。
        如果指定的键不存在，返回值是 0（表示没有键被删除）。
    """
    date_only = datetime.now().strftime('%Y%m%d')   # 例如 20250115
    key = f"{date_only}-{user_name}"    # 例如 20250115-中东悍匪    
    
    result = await redis_client.delete(key)
    print(f"从 Redis 删除数据的result为: {result}")
    if result:
        print(f"键名为 {key} 的数据已删除！")
    else:
        print(f"键名为 {key} 的数据不存在！")

if __name__ == "__main__":
    # 命令行参数解析，命令行执行示例：python redis_exist_and_delete.py get
    parser = argparse.ArgumentParser(description="处理用户数据。")
    parser.add_argument(
        "action",
        choices=["get", "delete"],
        help="要执行的操作：'get' 获取数据，'delete' 删除数据"
    )
    args = parser.parse_args()
    
    # 设置用户名称
    user_name = "中东土匪"
    if args.action == "get":
        asyncio.run(get_data(user_name))    # 获取对应数据
    elif args.action == "delete":
        asyncio.run(delete_data(user_name)) # 删除对应数据