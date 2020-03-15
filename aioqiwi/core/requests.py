import asyncio
import logging
from typing import List, Optional, Type, TypeVar, Union, AnyStr

from pydantic import ValidationError

from ..exceptions import (
    AioqiwiError, E,
    JSONDeserializeError,
    ModelValidationError,
    ReadDataProcessError,
)

from . import handler, returns
from .connectors import Connector, ConnectorException, Response
from .tooling import datetime, json

M = TypeVar("M")
R = Optional[Union[bytes, str, M, List[M]]]

logger = logging.getLogger("aioqiwi.requests")
core_loop = asyncio.get_event_loop()


class Toolset:
    connector: Optional[Connector] = None
    """Custom connector for making requests, if None AiohttpConnector will be used"""

    return_type: returns.ReturnType = returns.ReturnType.MODEL
    """Returns (noun) as aioqiwi models by default"""

    json_module: json.JsonModule = json.JsonModule("json")
    """JSON deserialization/serialization manager"""

    datetime_module: datetime.DatetimeModule = datetime.DatetimeModule()
    """Qiwi API datetime defaults tool"""

    handler_manager: Optional[handler.HandlerManager] = None
    """handler_manager class. sooner will be bind if needed"""


default_toolset = Toolset()


class Requests:
    _error_model: Optional[Type[E]] = None

    handler_manager: Optional[handler.HandlerManager] = None
    """handler_manager class. sooner will be bind if needed"""

    def __init__(
        self,
        auth: Optional[str],
        timeout: Optional[Union[float, int]] = None,
        *,
        send_type: Optional[str] = None,
        acpt_type: Optional[str] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
    ):
        headers = {
            "Accept": acpt_type or "application/json",
            "Content-type": send_type or "application/json",
            "Authorization": f"Bearer {auth}"
            if auth
            else None,  # maps api does not require authorization
        }

        self._tools = default_toolset

        if event_loop is None:
            event_loop = core_loop

        if self._tools.connector is None:
            from aioqiwi.core.connectors.aiohttp import AiohttpConnector

            self._tools.connector = AiohttpConnector.new(
                timeout=timeout,
                default_headers=self._filter_dict(headers),
                loop=event_loop,
            )

        self.loop = event_loop

    @property
    def tools(self) -> Toolset:
        return self._tools

    @tools.setter
    def tools(self, value: Toolset):
        if not isinstance(value, Toolset):
            raise TypeError(f"`tools` can be nothing but ToolSet, got {type(value)} instead")
        self._tools = value

    async def _read_response(self, response: Response) -> AnyStr:
        try:
            data = await response.read()

            if response.status_code not in response.status_codes_success:
                raise AioqiwiError.with_error_model(
                    self._error_model,
                    self._tools.json_module.deserialize(data)
                )

        except ConnectorException as exc:
            raise ReadDataProcessError("Connector error occurred while reading response") from exc
        finally:
            await response.close()

        return data

    async def _make_return(
        self,
        response: Response,
        current_model: Optional[Type[M]] = None,
        forces_return_type: Optional[returns.ReturnType] = None,
    ) -> R[M]:
        """
        Make return with respect to current_model and return type factors
        :param response: aiohttp current response from stream
        :param current_model: model to initialize
        :param forces_return_type: current return type
        """
        data = await self._read_response(response)
        if (
                forces_return_type and forces_return_type is returns.ReturnType.NOTHING
        ) or self._tools.return_type is returns.ReturnType.NOTHING:
            return

        if (
            forces_return_type and forces_return_type is returns.ReturnType.READ_DATA
        ) or self._tools.return_type is returns.ReturnType.READ_DATA:
            return data

        try:
            json_data = self._tools.json_module.deserialize(data)
        except (TypeError,) as exc:
            logger.error(exc)
            raise JSONDeserializeError("JSON parsing error")

        if (
            forces_return_type and forces_return_type is returns.ReturnType.JSON
        ) or self._tools.return_type is returns.ReturnType.JSON:
            return json_data

        try:
            if forces_return_type and forces_return_type is returns.ReturnType.LIST_OF_MODELS:
                return [current_model(**obj) for obj in json_data]
            else:
                return current_model(**json_data)

        except ValidationError as error:
            raise ModelValidationError(error.json())

    @classmethod
    def _filter_dict(cls, dictionary: dict):
        """
        Pop NoneType values and convert everything to str, designed?for=params
        :param dictionary: source dict
        :return: filtered dict
        """
        return {k: str(v) for k, v in dictionary.items() if v is not None}

    @property
    def hm(self) -> handler.HandlerManager:
        """Handler manager"""
        if self._tools.handler_manager is None:
            raise ValueError(f"{self!r} does not have a initialized handler_manager")
        return self._tools.handler_manager

    async def close(self):
        if self._tools.connector is not None:
            await self._tools.connector.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
