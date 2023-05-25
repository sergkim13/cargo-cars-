from abc import ABC, abstractmethod


class AbstractCache(ABC):
    @abstractmethod
    def __init__(self, cache_client) -> None:
        self.cache_client = cache_client

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def set(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def clear(self, *args, **kwargs):
        raise NotImplementedError
