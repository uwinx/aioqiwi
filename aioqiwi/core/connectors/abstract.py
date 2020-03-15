import abc
import asyncio
from typing import AnyStr, ClassVar, Dict, List, Optional, Union


class Response(metaclass=abc.ABCMeta):
    status_code: ClassVar[int]
    status_codes_success: ClassVar[List[int]]

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


class Connector(metaclass=abc.ABCMeta):
    @classmethod
    def new(
        cls,
        timeout: Union[int, float],
        default_headers: Dict[str, str],
        loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        raise NotImplementedError

    async def request(self, method: str, url: str, **kwargs) -> Response:
        """
        Should implement http request for particular method
        """
        raise NotImplementedError

    async def close(self):
        """
        Should "close" connector, can be used to close all current streams etc.
        Can be called several times, `closed` flag may be required.
        """
        raise NotImplementedError
