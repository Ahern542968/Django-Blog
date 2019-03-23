import time
import functools
from collections import OrderedDict

from django.core.cache import cache


class LRUCacheDict(object):
    def __init__(self, max_size=1024, expiration=60*60*24):
        self.max_size = max_size
        self.expiration = expiration
        self._cache = {}
        self._access_records = OrderedDict()
        self._expire_records = OrderedDict()

    def __setitem__(self, key, value):
        now = int(time.time())
        self.__delete__(key)

        self._cache[key] = value
        self._access_records[key] = now
        self._expire_records[key] = now + self.expiration

        self.cleanup()

    def __getitem__(self, key):
        now = int(time.time())
        del self._access_records[key]
        self._access_records[key] = now
        self.cleanup()

        return self._cache[key]

    def __contains__(self, key):
        self.cleanup()
        return key in self._cache

    def __delete__(self, key):
        if key in self._cache:
            del self._cache[key]
            del self._access_records
            del self._expire_records

    def cleanup(self):
        if self.expiration is None:
            return None

        pending_delete_keys = []
        now = int(time.time())
        for key, value in self._expire_records.items():
            if value < now:
                pending_delete_keys.append(key)

        for del_key in pending_delete_keys:
            self.__delete__(del_key)

        while len(self._cache) > self.max_size:
            for key in self._access_records:
                self.__delete__(key)
                break


def cache_it(max_size=1024, expiration=60*60*24):
    CACHE = LRUCacheDict(max_size=max_size, expiration=expiration)

    def wrapper(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            key = repr(*args, **kwargs)
            try:
                result = CACHE[key]
            except KeyError:
                result = func(*args, **kwargs)
                CACHE[key] = result
            return result
        return inner
    return wrapper


def redis_cache(key, timeout):
    def wrapper(fun):
        def inner(*args, **kwargs):
            if cache.get(key):
                result = cache.get(key)
            else:
                result = fun(*args, **kwargs)
                cache.set(key, result, timeout)
            return result
        return inner
    return wrapper
