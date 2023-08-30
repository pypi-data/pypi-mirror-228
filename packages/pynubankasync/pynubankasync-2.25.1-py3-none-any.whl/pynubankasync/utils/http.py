from httpx import AsyncClient, Response
from httpx_pkcs12 import create_ssl_context

from pynubankasync import NuRequestException


class HttpClient:
    def __init__(self):
        self._cert = None
        self._headers = {
            "Content-Type": "application/json",
            "X-Correlation-Id": "and-7-86-2-1000005524.9twu3pgr",
            "User-Agent": "pynubankasync Client - https://github.com/andreroggeri/pynubankasync",
        }

    def set_cert_data(self, cert_data: bytes):
        self._cert = create_ssl_context(cert_data, None)

    def set_header(self, name: str, value: str):
        self._headers[name] = value

    def remove_header(self, name: str):
        self._headers.pop(name)

    def get_header(self, name: str):
        return self._headers.get(name)

    def _handle_response(self, response: Response) -> dict:
        if response.status_code != 200:
            raise NuRequestException(response)

        return response.json()

    async def raw_get(self, url: str) -> Response:
        async with AsyncClient(verify=self._cert) as client:
            return await client.get(url, headers=self._headers)

    async def raw_post(self, url: str, json: dict) -> Response:
        async with AsyncClient(verify=self._cert) as client:
            return await client.post(url, headers=self._headers, json=json)

    async def get(self, url: str) -> dict:
        return self._handle_response(await self.raw_get(url))

    async def post(self, url: str, json: dict) -> dict:
        return self._handle_response(await self.raw_post(url, json=json))
