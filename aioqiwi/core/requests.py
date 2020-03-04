import asyncio
import logging
from typing import List, Optional, Type, TypeVar, Union

from aiohttp import client, client_exceptions
from pydantic import ValidationError

from ..exceptions import (
    JSONDeserializeError,
    ModelValidationError,
    ReadDataProcessError,
)
from . import datetime, handler, json, returns

M = TypeVar("M")

logger = logging.getLogger("aioqiwi.requests")
core_loop = asyncio.get_event_loop()


class Requests:
    return_type = returns.ReturnType.MODEL
    """Returns as aioqiwi models by default"""

    json_module = json.JsonModule("json")
    """JSON deserialization/serialization manager"""

    datetime_module = datetime.DatetimeModule()
    """Qiwi API datetime defaults tool"""

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

        self.timeout = client.ClientTimeout(total=timeout or 60)

        if event_loop is None:
            event_loop = core_loop

        self.loop = event_loop
        self._session = client.ClientSession(
            headers=self.params_filter(headers), timeout=self.timeout, loop=event_loop
        )

    async def make_return(
        self,
        response: client.ClientResponse,
        current_model: Optional[Type[M]] = None,
        forces_return_type: Optional[returns.ReturnType] = None,
    ) -> Optional[Union[M, List[M], bytes, str]]:
        """
        Make return with respect to current_model and return type factors
        :param response: aiohttp current response from stream
        :param current_model: model to initialize
        :param forces_return_type: current return type
        """

        try:
            data = await response.read()
        except client_exceptions.ClientConnectionError as exc:
            raise ReadDataProcessError().with_traceback(exc.__traceback__)

        if not data:
            raise ReadDataProcessError("Empty response data was obtained")

        if (
            forces_return_type and forces_return_type.READ_DATA
        ) or self.return_type is returns.ReturnType.READ_DATA:
            return data

        try:
            json_data = self.json_module.deserialize(data)
        except (TypeError,) as exc:
            logger.error(exc)
            raise JSONDeserializeError("JSON parsing error")

        if (
            forces_return_type and forces_return_type.JSON
        ) or self.return_type is returns.ReturnType.JSON:
            return json_data

        try:
            if forces_return_type and forces_return_type.LIST_OF_MODELS:
                return [
                    current_model.__init__(**obj) for obj in json_data  # type: ignore
                ]
            else:
                return current_model.__init__(**json_data)  # type: ignore

        except ValidationError as error:
            raise ModelValidationError(error.json())

    @classmethod
    def params_filter(cls, dictionary: dict):
        """
        Pop NoneType values and convert everything to str, designed?for=params
        :param dictionary: source dict
        :return: filtered dict
        """
        return {k: str(v) for k, v in dictionary.items() if v is not None}

    @property
    def hm(self) -> handler.HandlerManager:
        """Handler manager"""
        if self.handler_manager is None:
            raise ValueError(f"{self!r} does not have a initialized handler_manager")
        return self.handler_manager

    async def close(self):
        await self._session.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
