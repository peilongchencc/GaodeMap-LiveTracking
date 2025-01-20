"""
Description: 
Notes: 
Requirements: pip install redis[asyncio]
"""
import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

REDIS_URL = "redis://localhost:6379"
REDIS_PASSWORD = "123456"  # Redis 密码，如果有则设置
MAX_CONNECTIONS = 1000  # Redis 最大连接数

# 数据库指标
DB_INDEXES = {
    1: "user_status",  # 用户状态
    2: "scheduled_tasks_messages",  # 定时任务消息
    3: "user_map_message"  # 用户映射消息
}

class RedisManager:
    """
    Redis 管理器类，负责管理 Redis 的连接池和客户端。
    """
    connection_pools = {}

    @staticmethod
    def initialize_connection_pools():
        """
        初始化所有定义的 Redis 数据库索引的连接池。

        通过 DB_INDEXES 创建每个索引的连接池并存储在 connection_pools 中。
        """
        RedisManager.connection_pools = {
            index: ConnectionPool.from_url(
                REDIS_URL,
                db=index,
                password=REDIS_PASSWORD,
                max_connections=MAX_CONNECTIONS,
                decode_responses=True
            ) for index in DB_INDEXES
        }

    @staticmethod
    def get_redis_client(db_index):
        """
        获取指定数据库索引的 Redis 客户端。

        Args:
            db_index (int): Redis 数据库索引。

        Returns:
            redis.Redis: Redis 客户端实例。

        Raises:
            ValueError: 当提供的数据库索引不被支持时抛出。
        """
        if db_index not in RedisManager.connection_pools:
            raise ValueError(f"Unsupported DB index: {db_index}")
        return redis.Redis(connection_pool=RedisManager.connection_pools[db_index])

# 脚本运行时初始化连接池
try:
    RedisManager.initialize_connection_pools()
except Exception as e:
    print(f"Error initializing Redis connection pools: {e}")