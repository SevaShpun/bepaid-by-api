import aiohttp
import requests
from typing import Optional


DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
}


class HttpClient:
    """
    ✅ Пример использования:
    
    Асинхронный:
    
        import asyncio

        async def main():
            async with HttpClient() as client:
                response = await client.async_get("https://example.com")
                text = await response.text()
                print(text)

        asyncio.run(main())

    Синхронный:
    
        client = HttpClient()
        response = client.get("https://example.com")
        print(response.text)
    """
    def __init__(self, headers: dict = DEFAULT_HEADERS):
        self._session: Optional[aiohttp.ClientSession] = None
        self.headers = headers

    async def __aenter__(self):
        self._session = aiohttp.ClientSession(headers=self.headers)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._session:
            await self._session.close()

    # -------- Async methods --------

    async def async_get(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        self._ensure_session()
        return await self._session.get(url, **kwargs)

    async def async_post(self, url: str, **kwargs) -> aiohttp.ClientResponse:
        self._ensure_session()
        return await self._session.post(url, **kwargs)

    def _ensure_session(self):
        if not self._session:
            raise RuntimeError("ClientSession is not initialized. Use 'async with HttpClient()'.")

    # -------- Sync methods --------

    def get(self, url: str, **kwargs) -> requests.Response:
        return requests.get(url, headers=self.headers, **kwargs)

    def post(self, url: str, **kwargs) -> requests.Response:
        return requests.post(url, headers=self.headers, **kwargs)
