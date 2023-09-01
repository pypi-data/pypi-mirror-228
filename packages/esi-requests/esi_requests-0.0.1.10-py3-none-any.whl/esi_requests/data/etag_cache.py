from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Union

from .cache import SqliteCache

if TYPE_CHECKING:
    from esi_requests.models import ESIResponse


@dataclass
class _ETagCacheEntry:
    etag: str
    response: "ESIResponse"


class ETagCache:
    """Caches ETags and their associated ESIResponses. 
    Cache keys are URLs, and values are ``_ETagCacheEntry`` objects.

    Note:
        The cache object is lazy-loaded, so it will not be created until first get/set.
    """
    def __init__(self) -> None:
        # self.cache = SqliteCache("request_cache", table="etag")
        self.cache: SqliteCache = None
        self.enabled = True
    
    def get(self, url: str, default: Any = None) -> "_ETagCacheEntry":
        """Gets the ETag response for a given URL."""
        if not self.enabled:
            return default
        if self.cache is None:
            self.cache = SqliteCache("request_cache", table="etag")
        return self.cache.get(url, default)

    def set(self, url: str, etag: str, response: "ESIResponse", expires: Union[str, int]):
        """Sets the ETag response for a given URL."""
        if not self.enabled:
            return  # if cache disabled, do nothing
        if self.cache is None:
            self.cache = SqliteCache("request_cache", table="etag")
        entry = _ETagCacheEntry(etag, response)
        self.cache.set(url, entry, expires)
