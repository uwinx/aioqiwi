from __future__ import annotations

import asyncio
from typing import Dict, Optional, Union

from aiohttp import client

from .abstract import Connector, ConnectorException, Response


class AiohttpResponse(Response):
    status_codes_success = [200, 201]

    def __init__(self, response: client.ClientResponse):
        self._resp = response
        self.status_code = response.status

    async def read(self) -> bytes:
        try:
            return await self._resp.read()
        except client.ClientConnectionError as exc:
            raise ConnectorException("Connector exception occurred") from exc

    async def close(self):
        await self._resp.release()


class AiohttpConnector(Connector):
    _client: client.ClientSession

    @classmethod
    def new(
        cls,
        timeout: Union[int, float],
        default_headers: Dict[str, str],
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ) -> AiohttpConnector:
        obj = cls()
        timeout = client.ClientTimeout(total=timeout or 60)
        obj._client = client.ClientSession(
            timeout=timeout, headers=default_headers, loop=loop
        )
        return obj

    async def request(self, method: str, url: str, **kwargs) -> AiohttpResponse:
        response = await self._client.request(method, url, **kwargs)
        return AiohttpResponse(response)

    async def close(self):
        if not self._client.closed:
            return await self._client.close()
