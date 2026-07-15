"""
Redis Cache Service
Provides caching layer for image features and search results
"""

import json
import logging
from typing import Optional, List, Any

logger = logging.getLogger(__name__)

try:
    import redis
except ImportError:
    redis = None  # type: ignore[assignment]


class CacheService:
    """Service for caching with Redis"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        ttl: int = 3600,
    ):
        """
        Initialize Redis cache connection

        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            ttl: Default TTL in seconds
        """
        self.ttl = ttl
        self.client: Optional[Any] = None

        if redis is None:
            logger.warning("redis package not installed, caching disabled")
            return

        try:
            self.client = redis.Redis(
                host=host, port=port, db=db, decode_responses=True
            )
            self.client.ping()
            logger.info(f"Redis cache connected ({host}:{port})")
        except Exception as e:
            logger.warning(f"Redis not available, caching disabled: {e}")
            self.client = None

    @property
    def is_available(self) -> bool:
        return self.client is not None

    def get(self, key: str) -> Optional[Any]:
        if not self.is_available:
            return None
        try:
            data = self.client.get(key)  # type: ignore[union-attr]
            return json.loads(data) if data else None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        if not self.is_available:
            return False
        try:
            self.client.setex(  # type: ignore[union-attr]
                key, ttl or self.ttl, json.dumps(value)
            )
            return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        if not self.is_available:
            return False
        try:
            self.client.delete(key)  # type: ignore[union-attr]
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False

    def cache_features(self, image_id: str, features: List[float]) -> bool:
        return self.set(f"features:{image_id}", features)

    def get_cached_features(self, image_id: str) -> Optional[List[float]]:
        return self.get(f"features:{image_id}")

    def cache_search_results(
        self, query_hash: str, results: List[Any]
    ) -> bool:
        return self.set(f"search:{query_hash}", results, ttl=300)

    def get_cached_search(self, query_hash: str) -> Optional[List[Any]]:
        return self.get(f"search:{query_hash}")
