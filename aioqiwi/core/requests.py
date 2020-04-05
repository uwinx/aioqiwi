import asyncio
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

DEFAULT_TIMEOUT = 60.0

M = TypeVar("M")
R = Optional[Union[bytes, str, M, List[M]]]

core_loop = asyncio.get_event_loop()


class Toolset:
    return_type: returns.ReturnType = returns.ReturnType.MODEL
    """Returns (noun) as aioqiwi models by default"""

    json_module: json.JsonModule = json.JsonModule("json")
    """JSON deserialization/serialization manager"""

    datetime_module: datetime.DatetimeModule = datetime.DatetimeModule()
    """Qiwi API datetime defaults tool"""


default_toolset = Toolset()


class Requests:
    _error_model: Optional[Type[E]] = None

    handler_manager: Optional[handler.HandlerManager] = None
    """handler_manager class. sooner will be bind if needed"""

    def __init__(
        self,
        auth: Optional[str],
        timeout: Optional[float] = None,
        *,
        send_type: Optional[str] = None,
        acpt_type: Optional[str] = None,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        connector: Optional[Connector] = None,
        close_connector_at_aexit: bool = True,
        handler_manager: Optional[handler.HandlerManager] = None,
    ):
        headers = {
            "Accept": acpt_type or "application/json",
            "Content-type": send_type or "application/json",
            "Authorization": f"Bearer {auth}"
            if auth
            else None,  # maps api does not require authorization
            "User-Agent": "aioqiwi/1.x"
        }

        self._tools = default_toolset

        if event_loop is None:
            event_loop = core_loop

        if connector is None:
            default_headers = self._filter_dict(headers)

            from aioqiwi.core.connectors.asyncio import AsyncioConnector

            connector = AsyncioConnector(
                timeout=timeout or DEFAULT_TIMEOUT,
                default_headers=default_headers,
                loop=event_loop,
            )

        if handler_manager is None:
            handler_manager = handler.HandlerManager(loop=event_loop)

        self.handler_manager = handler_manager

        self._connector = connector
        self.close_at_aexit = close_connector_at_aexit
        self.loop = event_loop

    @property
    def tools(self) -> Toolset:
        return self._tools

    @tools.setter
    def tools(self, value: Toolset):
        if not isinstance(value, Toolset):
            raise TypeError(f"`tools` can be nothing but ToolSet, got {type(value)} instead")
        self._tools = value

    @property
    def connector(self) -> Connector:
        return self._connector

    @connector.setter
    def connector(self, new_connector: Union[Type[Connector], Connector]):
        if issubclass(new_connector, Connector):  # expect connector to be class
            self._connector = new_connector.from_connector(self._connector)
        else:
            self._connector = new_connector

    async def _read_response(self, response: Response) -> AnyStr:
        try:
            data = await response.read()

            if response.status_code not in response.status_codes_success:
                try:
                    err = AioqiwiError.with_error_model(
                        self._error_model,
                        self._tools.json_module.deserialize(data)
                    )
                    exc = None
                except (TypeError, ValueError) as occ_exc:
                    err = AioqiwiError()
                    exc = occ_exc
                raise err from exc

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
        except (TypeError, ValueError):
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
        """Handler manager but not :thinking_face:"""
        return self.handler_manager

    async def close(self):
        await self.connector.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.close_at_aexit:
            await self.close()
