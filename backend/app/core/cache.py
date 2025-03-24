# backend/app/core/cache.py
import time
import json
from typing import Any, Dict, Optional, Callable
import logging
import functools

from app.config import settings

logger = logging.getLogger(__name__)

# Simple in-memory cache
cache_store = {}

def cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments"""
    key_parts = [str(arg) for arg in args]
    key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
    return ":".join(key_parts)

def cache(ttl: int = None):
    """
    Cache decorator for expensive function calls
    
    Args:
        ttl: Time-to-live in seconds (None means use default from settings)
    """
    ttl = ttl if ttl is not None else settings.CACHE_TTL
    
    def decorator(func: Callable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if not settings.CACHE_ENABLED:
                return await func(*args, **kwargs)
            
            # Generate cache key
            key = f"{func.__module__}:{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Check if result is in cache and not expired
            if key in cache_store:
                entry = cache_store[key]
                if entry["expires"] > time.time():
                    logger.debug(f"Cache hit: {key}")
                    return entry["value"]
                else:
                    # Remove expired entry
                    logger.debug(f"Cache expired: {key}")
                    del cache_store[key]
            
            # Call function and cache result
            result = await func(*args, **kwargs)
            
            cache_store[key] = {
                "value": result,
                "expires": time.time() + ttl
            }
            logger.debug(f"Cache set: {key}")
            
            return result
        
        return wrapper
    
    return decorator

def clear_cache():
    """Clear the entire cache"""
    global cache_store
    cache_store = {}
    logger.info("Cache cleared")

def remove_from_cache(key_pattern: str):
    """
    Remove specific entries from cache
    
    Args:
        key_pattern: Pattern to match against cache keys
    """
    removed = 0
    for key in list(cache_store.keys()):
        if key_pattern in key:
            del cache_store[key]
            removed += 1
    
    logger.info(f"Removed {removed} entries from cache matching: {key_pattern}")