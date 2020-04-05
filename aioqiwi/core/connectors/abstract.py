import abc
import asyncio
from typing import AnyStr, ClassVar, List, Optional, TypeVar, Dict, Mapping

T = TypeVar("T")


class Response(abc.ABC):
    status_code: int
    status_codes_success: ClassVar[List[int]]
    content_type: str

    async def read(self) -> AnyStr:
        """
        Should return json-serializable bytes or str object
        """
        raise NotImplementedError

    async def close(self):
        """
        Will be called after reading response [Guaranteed in core.request.Requests::make_return]
        """
        raise NotImplementedError


class ConnectorException(Exception):
    ...


class Connector(abc.ABC):
    def __init__(
        self,
        timeout: float,
        default_headers: Mapping[str, str],
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        """
        :param timeout: request timeout should be float'able
        :param default_headers: flat [str,str] mapping
        :param loop: asyncio's abstract event loop compatible
        """
        self.timeout = timeout
        self.default_headers = default_headers
        self.loop = loop

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, str]] = None,
        data: Optional[AnyStr] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Response:
        """
        Should implement http request for particular method

        :param method: HTTP method
        :param url: URL string
        :param params: Dictionary of query holding parameters (e.g: url + "?" + key=val + sep)
        :param data: Request body
        :param headers: Dictionary holding headers
                        (default headers are in lower priority, this dict can overlap with default)
        :return: Implemented `Response` object
        """
        raise NotImplementedError

    async def close(self):
        """
        Should "close" connector, can be used to close all current streams etc.
        Can be called several times, `closed` flag may be required.
        """
        raise NotImplementedError

    @classmethod
    def from_connector(cls, connector: 'Connector') -> 'Connector':
        """
        Get current class' connector instance. Implemented method.
        :param connector: old connector to be replace
        """

        return cls(
            timeout=connector.timeout,
            default_headers=connector.default_headers,
            loop=connector.loop
        )
