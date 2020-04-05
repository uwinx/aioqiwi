import typing

from aiohttp import web

from . import returns
from .tooling import json

if typing.TYPE_CHECKING:
    from .handler import HandlerManager


class BaseWebHookView(web.View):
    event_delivery_type = returns.ReturnType.MODEL
    """event delivery type"""

    json_module = json.JsonModule("json")
    """JSON deserialization/serialization manager"""

    app_key_check_ip: typing.Optional[str] = None
    """app_key_check_ip stores key to a storage"""

    app_key_handler_manager: typing.Optional[str] = None
    """app_key_handler_manager"""

    def _check_ip(self, ip: str):
        """_check_ip checks if given IP is in set of allowed ones"""
        raise NotImplementedError

    def parse_update(self):
        """parse_update method that deals with marshaling json"""
        raise NotImplementedError

    def validate_ip(self):
        # pulled from aiogram.dispatcher.webhook IP-validator
        if self.request.app.get(self.app_key_check_ip):
            ip_address, accept = self.check_ip()
            if not accept:
                raise web.HTTPUnauthorized()

    def check_ip(self):
        forwarded_for = self.request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for, self._check_ip(forwarded_for)

        peer_name = self.request.transport.get_extra_info("peername")

        if peer_name is not None:
            host, _ = peer_name
            return host, self._check_ip(host)

        return None, False

    async def post(self):
        """
        Process POST request with basic IP validation.
        """
        self.validate_ip()

        update = await self.parse_update()
        await self.handler_manager.process_event(update)

        return web.Response(text="ok", status=200)

    @property
    def handler_manager(self) -> "HandlerManager":
        return self.request.app.get(self.app_key_handler_manager)  # type: ignore
