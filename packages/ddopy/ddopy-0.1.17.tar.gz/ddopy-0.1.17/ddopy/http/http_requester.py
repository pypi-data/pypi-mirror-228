"""
This module contains HttpRequester class which is used to send HTTP requests.
"""
import aiohttp
import json

class HttpRequester:
    def __init__(self):
        self._base_url = None
        self._headers = {}
        self._session = None

    def set_base_url(self, url):
        self._base_url = url

    def add_header(self, key, value):
        self._headers[key] = value

    async def _get_session(self):
        if self._session is None:
            self._session = aiohttp.ClientSession(headers=self._headers)
        return self._session

    async def close_session(self):
        if self._session:
            await self._session.close()
            self._session = None

    async def get_request(self, relative_url=""):
        if self._base_url is None:
            raise Exception("Base URL is not set. Call set_base_url() method first.")

        url = f"{self._base_url}/{relative_url.lstrip('/')}".rstrip("/")

        session = await self._get_session()

        async with session.get(url) as response:
            await response.read()
            return response

    async def post_request(self, payload, relative_url=""):
        if self._base_url is None:
            raise Exception("Base URL is not set. Call set_base_url() method first.")

        url = f"{self._base_url}/{relative_url.lstrip('/')}".rstrip("/")

        session = await self._get_session()

        async with session.post(url, data=json.dumps(payload)) as response:
            await response.read()
            return response
