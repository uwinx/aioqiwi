import asyncio
from urllib.parse import urlparse, ParseResult, urlencode
from typing import Tuple, AnyStr, Optional, Dict, Deque, Set, Mapping
from collections import deque
from itertools import chain

from .abstract import Connector, ConnectorException, Response

StreamType = Tuple[asyncio.StreamReader, asyncio.StreamWriter]

HTTP_DEFAULT_PORT = 80
HTTPS_DEFAULT_PORT = 443


class AsyncioResponse(Response):
    status_code = -1
    status_codes_success = [200, 201]
    content_type = "none"

    _r: asyncio.StreamReader
    _is_read = False

    @property
    def is_read(self) -> bool:
        return self._is_read

    @classmethod
    async def init_status_code(cls, reader: asyncio.StreamReader):
        self = cls()
        _, status_code, *_ = (await reader.readline()).split(maxsplit=2)
        self.status_code = int(status_code)
        self._r = reader
        self._is_read = False
        return self

    async def read(self) -> AnyStr:
        if self.is_read:
            raise ConnectorException("Stream has been read already and cannot be read again")
        try:
            # Headers are duplicated to ease parsing process.
            # `lheaders` is lower-case plain-headers and `headers` is original
            headers = await self._r.readuntil(b"\r\n\r\n")
            lheaders = headers.lower()
            if headers[-4:] != b"\r\n\r\n":
                raise ConnectorException()
        except (asyncio.TimeoutError, asyncio.IncompleteReadError) as exc:
            raise ConnectorException() from exc

        content_type_loc = lheaders.index(b"content-type") + 13
        self.content_type = headers[content_type_loc:lheaders.index(b"\r", content_type_loc)].decode()

        index = lheaders.index(b"content-length") + 15
        try:
            return await self._r.readexactly(int(headers[index:lheaders.index(b"\r", index)]))
        except asyncio.LimitOverrunError as exc:
            raise ConnectorException() from exc
        finally:
            self._is_read = True

    async def close(self):
        # we do not care if stream is open or closed
        # connector is responsible for stream managing in this implementation
        pass


def make_headers(d: Mapping[str, str]) -> bytes:
    """
    Header keys are case insensitive, aioqiwi prefers lower-case keys over mixed ones
    """

    return b"\r\n".join(
        f"{_k}: {_v}".encode() for _k, _v in d.items()
    ) + b"\r\n"


class AsyncioConnector(Connector):
    def __init__(
        self,
        timeout: float,
        default_headers: Mapping[str, str],
        loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        # Note: timeout covers only write/status sniff(first read) parts
        super().__init__(timeout, default_headers, loop)

        self._closed = False
        # we use stream req-time semaphore
        self._semaphore = asyncio.Semaphore()

        # keep some connections' underlying socket open with the help of the following dss
        self._connections_deque: Deque[StreamType] = deque()
        self._busy_connections: Set[StreamType] = set()

    def form_http_request(
        self,
        method: str,
        url_parsed: ParseResult,
        params: Optional[Dict[str, str]] = None,
        data: Optional[AnyStr] = None,
        use_default_headers: bool = True,
        headers: Optional[Dict[str, str]] = None
    ) -> bytes:
        """
        Form HTTP plain request with {method path ver}\r\n{headers \r\n by \r\n}\r\n{body or nothing}
        :param method: HTTP method must be passed
        :param url_parsed: urllib.urlparse result getting string
        :param params: query parameters of request, path will be extended
        :param data: body of request
        :param use_default_headers: flag meaning if default headers should be updated for request with current headers
        :param headers: current request headers
        :return: encoded http plain text for request
        """
        path = url_parsed.path

        if params:
            path += "?" + urlencode(params)

        http_request = b"%b %b HTTP/1.1\r\n" % (
            method.encode(),
            path.encode()
        )

        plain_headers = b""
        if use_default_headers:
            temp = self.default_headers.copy()
            if headers:
                temp.update(**headers)
            plain_headers += make_headers(temp)
            del temp
        elif headers:
            plain_headers += make_headers(headers)

        # generics and auto headers
        if data and len(data) != 0:
            plain_headers += b"content-length: %i\r\n" % (len(data) if data else 0)
        plain_headers += b"host: %b\r\n" % url_parsed.hostname.encode()

        http_request += plain_headers + b"\r\n"  # end of headers

        if data:
            http_request += (
                data
                if isinstance(data, bytes)
                else data.encode()
                if isinstance(data, str)
                else b""
            )

        return http_request

    async def _request(self, rw: Optional[StreamType], http_request: bytes, parsed: ParseResult):
        if rw is None:
            # assume scheme to be either http and http(s) if https asyncio will use different transport
            use_ssl = parsed.scheme.endswith("s")

            rw = await asyncio.open_connection(
                parsed.hostname,
                # use protocol default ports
                parsed.port or (HTTPS_DEFAULT_PORT if use_ssl else HTTP_DEFAULT_PORT),
                loop=self.loop,
                ssl=use_ssl,
            )

        r, w = rw

        w.write(http_request)
        await w.drain()
        return await AsyncioResponse.init_status_code(r)

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, str]] = None,
        data: Optional[AnyStr] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> AsyncioResponse:
        """
        Implements Connector::request
        """
        parsed: ParseResult = urlparse(url)

        await self._semaphore.acquire()
        rw = self._connections_deque.popleft() if self._connections_deque else None
        self._busy_connections.add(rw)
        try:
            http_request = self.form_http_request(method, parsed, params, data, True, headers)

            # we expect task cancellation so we don't use asyncio.shield
            return await asyncio.wait_for(
                self._request(rw, http_request, parsed),
                timeout=self.timeout,
                loop=self.loop,
            )

        finally:
            self._busy_connections.discard(rw)
            self._connections_deque.append(rw)
            self._semaphore.release()

    async def close(self):
        """
        Close (and wait till close) all writers from reader/writers pair
        :return:
        """
        if self._closed:
            return

        self._closed = True

        async def _close(_: asyncio.StreamReader, w: asyncio.StreamWriter):
            w.close()
            await w.wait_closed()

        await asyncio.gather(*(_close(*rw) for rw in chain(
            self._connections_deque, self._busy_connections) if rw))

        self._connections_deque = deque([None] * len(self._connections_deque))
        self._busy_connections.clear()
