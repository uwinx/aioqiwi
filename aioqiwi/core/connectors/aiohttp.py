from __future__ import annotations

import asyncio
from typing import Optional, AnyStr, Mapping

from aiohttp import client, ClientTimeout

from .abstract import Connector, ConnectorException, Response


class AiohttpResponse(Response):
    status_codes_success = [200, 201]

    def __init__(self, response: client.ClientResponse):
        self._resp = response
        self.status_code = response.status
        self.content_type = response.content_type

    async def read(self) -> bytes:
        try:
            return await self._resp.read()
        except client.ClientConnectionError as exc:
            raise ConnectorException("Connector exception occurred") from exc

    async def close(self):
        await self._resp.release()


class AiohttpConnector(Connector):
    def __init__(
        self,
        timeout: float,
        default_headers: Mapping[str, str],
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        super().__init__(timeout, default_headers, loop)

        if isinstance(self.timeout, float):
            self._timeout = client.ClientTimeout(total=self.timeout)
        else:
            self._timeout = client.DEFAULT_TIMEOUT

    def _make_session(self):
        if self._client is None or self._client.closed:
            self._client = client.ClientSession(
                timeout=self._timeout, headers=self.default_headers, loop=self.loop
            )

        return self._client

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Mapping[str, str]] = None,
        data: Optional[AnyStr] = None,
        headers: Optional[Mapping[str, str]] = None
    ) -> AiohttpResponse:
        response = await self._make_session().request(method, url, params=params, data=data, headers=headers)
        return AiohttpResponse(response)

    async def close(self):
        if self._client is not None and not self._client.closed:
            await self._client.close()
