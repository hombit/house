from cachetools.func import ttl_cache


class ApiBasic:
    def __init__(self, cache_size:int, cache_ttl:int, **kwargs) -> None:
        self._cache_size = cache_size
        self._cache_ttl = cache_ttl
        self._call_kwargs = kwargs
        self._cache_decorator = ttl_cache(maxsize=cache_size, ttl=cache_ttl)
        self.get = self._cache_decorator(self._get)

    def __call__(self, *args, **kwargs) -> dict:
        kwargs.update(self._call_kwargs)
        return self.get(*args, **kwargs)

    @staticmethod
    def _get(*args, **kwargs) -> dict:
        raise NotImplemented('This class is basic, you should implement get method')
