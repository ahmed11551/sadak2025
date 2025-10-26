import redis
import json
import pickle
import hashlib
from typing import Any, Optional, Union, Dict, List
from datetime import datetime, timedelta
import logging
from functools import wraps
import asyncio

logger = logging.getLogger(__name__)

class CacheConfig:
    """Конфигурация кэша"""
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        decode_responses: bool = True,
        max_connections: int = 20,
        socket_timeout: int = 5,
        socket_connect_timeout: int = 5,
        retry_on_timeout: bool = True
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.decode_responses = decode_responses
        self.max_connections = max_connections
        self.socket_timeout = socket_timeout
        self.socket_connect_timeout = socket_connect_timeout
        self.retry_on_timeout = retry_on_timeout

class RedisCache:
    """Redis кэш с поддержкой различных типов данных"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self._client: Optional[redis.Redis] = None
        self._connection_pool: Optional[redis.ConnectionPool] = None
    
    def _get_client(self) -> redis.Redis:
        """Получает клиент Redis"""
        if self._client is None:
            self._connection_pool = redis.ConnectionPool(
                host=self.config.host,
                port=self.config.port,
                db=self.config.db,
                password=self.config.password,
                decode_responses=self.config.decode_responses,
                max_connections=self.config.max_connections,
                socket_timeout=self.config.socket_timeout,
                socket_connect_timeout=self.config.socket_connect_timeout,
                retry_on_timeout=self.config.retry_on_timeout
            )
            
            self._client = redis.Redis(connection_pool=self._connection_pool)
        
        return self._client
    
    def _make_key(self, key: str, namespace: str = "default") -> str:
        """Создает ключ с namespace"""
        return f"{namespace}:{key}"
    
    def _serialize(self, value: Any) -> str:
        """Сериализует значение"""
        if isinstance(value, (str, int, float, bool)):
            return json.dumps(value)
        else:
            return pickle.dumps(value).hex()
    
    def _deserialize(self, value: str, original_type: type = None) -> Any:
        """Десериализует значение"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            try:
                return pickle.loads(bytes.fromhex(value))
            except (ValueError, pickle.PickleError):
                return value
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        namespace: str = "default"
    ) -> bool:
        """Устанавливает значение в кэш"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            serialized_value = self._serialize(value)
            
            if ttl:
                return client.setex(cache_key, ttl, serialized_value)
            else:
                return client.set(cache_key, serialized_value)
                
        except Exception as e:
            logger.error(f"Error setting cache key {key}: {e}")
            return False
    
    def get(
        self,
        key: str,
        namespace: str = "default",
        default: Any = None
    ) -> Any:
        """Получает значение из кэша"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            value = client.get(cache_key)
            if value is None:
                return default
            
            return self._deserialize(value)
            
        except Exception as e:
            logger.error(f"Error getting cache key {key}: {e}")
            return default
    
    def delete(self, key: str, namespace: str = "default") -> bool:
        """Удаляет значение из кэша"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return bool(client.delete(cache_key))
            
        except Exception as e:
            logger.error(f"Error deleting cache key {key}: {e}")
            return False
    
    def exists(self, key: str, namespace: str = "default") -> bool:
        """Проверяет существование ключа"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return bool(client.exists(cache_key))
            
        except Exception as e:
            logger.error(f"Error checking cache key {key}: {e}")
            return False
    
    def ttl(self, key: str, namespace: str = "default") -> int:
        """Получает TTL ключа"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return client.ttl(cache_key)
            
        except Exception as e:
            logger.error(f"Error getting TTL for cache key {key}: {e}")
            return -1
    
    def expire(self, key: str, ttl: int, namespace: str = "default") -> bool:
        """Устанавливает TTL для ключа"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return bool(client.expire(cache_key, ttl))
            
        except Exception as e:
            logger.error(f"Error setting TTL for cache key {key}: {e}")
            return False
    
    def clear_namespace(self, namespace: str = "default") -> bool:
        """Очищает все ключи в namespace"""
        try:
            client = self._get_client()
            pattern = f"{namespace}:*"
            
            keys = client.keys(pattern)
            if keys:
                return bool(client.delete(*keys))
            
            return True
            
        except Exception as e:
            logger.error(f"Error clearing namespace {namespace}: {e}")
            return False
    
    def get_keys(self, pattern: str = "*", namespace: str = "default") -> List[str]:
        """Получает список ключей"""
        try:
            client = self._get_client()
            search_pattern = f"{namespace}:{pattern}"
            
            keys = client.keys(search_pattern)
            return [key.replace(f"{namespace}:", "") for key in keys]
            
        except Exception as e:
            logger.error(f"Error getting keys with pattern {pattern}: {e}")
            return []
    
    def increment(self, key: str, amount: int = 1, namespace: str = "default") -> int:
        """Увеличивает числовое значение"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return client.incrby(cache_key, amount)
            
        except Exception as e:
            logger.error(f"Error incrementing cache key {key}: {e}")
            return 0
    
    def decrement(self, key: str, amount: int = 1, namespace: str = "default") -> int:
        """Уменьшает числовое значение"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            return client.decrby(cache_key, amount)
            
        except Exception as e:
            logger.error(f"Error decrementing cache key {key}: {e}")
            return 0
    
    def hash_set(self, key: str, field: str, value: Any, namespace: str = "default") -> bool:
        """Устанавливает поле в hash"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            serialized_value = self._serialize(value)
            return bool(client.hset(cache_key, field, serialized_value))
            
        except Exception as e:
            logger.error(f"Error setting hash field {field} for key {key}: {e}")
            return False
    
    def hash_get(self, key: str, field: str, namespace: str = "default", default: Any = None) -> Any:
        """Получает поле из hash"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            value = client.hget(cache_key, field)
            if value is None:
                return default
            
            return self._deserialize(value)
            
        except Exception as e:
            logger.error(f"Error getting hash field {field} for key {key}: {e}")
            return default
    
    def hash_get_all(self, key: str, namespace: str = "default") -> Dict[str, Any]:
        """Получает все поля из hash"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            hash_data = client.hgetall(cache_key)
            return {field: self._deserialize(value) for field, value in hash_data.items()}
            
        except Exception as e:
            logger.error(f"Error getting all hash fields for key {key}: {e}")
            return {}
    
    def list_push(self, key: str, value: Any, namespace: str = "default") -> int:
        """Добавляет значение в список"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            serialized_value = self._serialize(value)
            return client.lpush(cache_key, serialized_value)
            
        except Exception as e:
            logger.error(f"Error pushing to list {key}: {e}")
            return 0
    
    def list_pop(self, key: str, namespace: str = "default", default: Any = None) -> Any:
        """Извлекает значение из списка"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            value = client.rpop(cache_key)
            if value is None:
                return default
            
            return self._deserialize(value)
            
        except Exception as e:
            logger.error(f"Error popping from list {key}: {e}")
            return default
    
    def list_get_all(self, key: str, namespace: str = "default") -> List[Any]:
        """Получает все значения из списка"""
        try:
            client = self._get_client()
            cache_key = self._make_key(key, namespace)
            
            values = client.lrange(cache_key, 0, -1)
            return [self._deserialize(value) for value in values]
            
        except Exception as e:
            logger.error(f"Error getting all list values for key {key}: {e}")
            return []
    
    def health_check(self) -> bool:
        """Проверяет здоровье кэша"""
        try:
            client = self._get_client()
            client.ping()
            return True
        except Exception as e:
            logger.error(f"Cache health check failed: {e}")
            return False

class CacheManager:
    """Менеджер кэша с различными стратегиями"""
    
    def __init__(self, cache: RedisCache):
        self.cache = cache
    
    def cache_result(
        self,
        ttl: int = 300,
        namespace: str = "default",
        key_func: callable = None
    ):
        """Декоратор для кэширования результатов функций"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                # Создаем ключ кэша
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = self._generate_key(func.__name__, args, kwargs)
                
                # Пытаемся получить из кэша
                cached_result = self.cache.get(cache_key, namespace)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result
                
                # Выполняем функцию
                logger.debug(f"Cache miss for {cache_key}")
                result = await func(*args, **kwargs)
                
                # Сохраняем в кэш
                self.cache.set(cache_key, result, ttl, namespace)
                
                return result
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                # Создаем ключ кэша
                if key_func:
                    cache_key = key_func(*args, **kwargs)
                else:
                    cache_key = self._generate_key(func.__name__, args, kwargs)
                
                # Пытаемся получить из кэша
                cached_result = self.cache.get(cache_key, namespace)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {cache_key}")
                    return cached_result
                
                # Выполняем функцию
                logger.debug(f"Cache miss for {cache_key}")
                result = func(*args, **kwargs)
                
                # Сохраняем в кэш
                self.cache.set(cache_key, result, ttl, namespace)
                
                return result
            
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def _generate_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Генерирует ключ кэша"""
        # Создаем строку из аргументов
        args_str = str(args) + str(sorted(kwargs.items()))
        
        # Создаем хэш
        hash_obj = hashlib.md5(args_str.encode())
        hash_str = hash_obj.hexdigest()
        
        return f"{func_name}:{hash_str}"
    
    def invalidate_pattern(self, pattern: str, namespace: str = "default"):
        """Инвалидирует кэш по паттерну"""
        keys = self.cache.get_keys(pattern, namespace)
        for key in keys:
            self.cache.delete(key, namespace)
    
    def warm_cache(self, func: callable, args_list: List[tuple], namespace: str = "default"):
        """Прогревает кэш"""
        for args in args_list:
            try:
                func(*args)
            except Exception as e:
                logger.error(f"Error warming cache for {func.__name__}: {e}")

# Глобальный экземпляр кэша
cache_config = CacheConfig()
cache = RedisCache(cache_config)
cache_manager = CacheManager(cache)
