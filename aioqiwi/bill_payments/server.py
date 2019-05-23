import ipaddress
import typing
import logging

from aiohttp import web

from ..models import bill_update, utils
from ..mixin import deserialize
from .crypto import get_auth_key

logger = logging.getLogger("aioqiwi")

logger.info(f"Deserialization tool: {deserialize.__name__}")

DEFAULT_QIWI_WEBHOOK_PATH = "/webhooks/qiwi/bills/"
DEFAULT_QIWI_ROUTER_NAME = "QIWI"

RESPONSE_TIMEOUT = 55

QIWI_IP_1 = ipaddress.IPv4Address("79.142.16.0/20")
QIWI_IP_2 = ipaddress.IPv4Address("91.232.230.0/23")
QIWI_IP_3 = ipaddress.IPv4Address("195.189.100.0/22")

allowed_ips = {QIWI_IP_1, QIWI_IP_2, QIWI_IP_3}


def _check_ip(ip: str) -> bool:
    address = ipaddress.IPv4Address(ip)
    return address in allowed_ips


def allow_ip(*ips: typing.Union[str, ipaddress.IPv4Network, ipaddress.IPv4Address]):
    for ip in ips:
        if isinstance(ip, ipaddress.IPv4Address):
            allowed_ips.add(ip)
        elif isinstance(ip, str):
            allowed_ips.add(ipaddress.IPv4Address(ip))
        elif isinstance(ip, ipaddress.IPv4Network):
            allowed_ips.update(ip.hosts())
        else:
            raise ValueError


class BaseWebHookView(web.View):
    async def x_api_validator(self):
        sha256 = self.request.headers.get("X-Api-Signature-SHA256")
        secret = self.request.app.get("_secret_key")
        bill = deserialize(await self.request.json()).get("bill", {})
        # rough __get_item__
        try:
            return (
                get_auth_key(
                    secret,
                    bill["amount"],
                    bill["status"],
                    bill["billId"],
                    bill["siteId"],
                )
                == sha256
            )
        except KeyError as exc:
            raise web.HTTPBadRequest(reason=f"{exc.args}")

    def validate_ip(self):
        # pulled from aiogram.dispatcher.webhook validator big thanks
        if self.request.app.get("_check_ip", False):
            ip_address, accept = self.check_ip()
            if not accept:
                raise web.HTTPUnauthorized()

    def check_ip(self):
        forwarded_for = self.request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for, _check_ip(forwarded_for)

        # For default method
        peer_name = self.request.transport.get_extra_info("peername")

        if peer_name is not None:
            host, _ = peer_name
            return host, _check_ip(host)

        # Not allowed and can't get client IP
        return None, False

    async def get(self):
        self.validate_ip()
        return web.Response(text="ok")

    async def head(self):
        self.validate_ip()
        return web.Response(text="ok")

    async def post(self):
        """
        Process POST request with validating and further deserialization and resolving
        :return: :class:``
        """
        self.validate_ip()

        if await self.x_api_validator():
            update = await self.parse_update()
            await self._resolve_update(update)

            return web.json_response(
                data={"error": "0"},
                status=200,
                headers={"Content-type": "application/json"}
            )

        return web.Response(status=0, headers={"Content-type": "application/json"})

    async def parse_update(self):
        """
        Deserialize update and create new update class
        :return: :class:``
        """
        data = await self.request.json()
        return utils.json_to_model(deserialize(data), bill_update.BillUpdate)

    async def _resolve_update(self, update):
        for callback, funcs, attr_eq in self.request.app["_dispatcher"]._handlers:
            if all(func(update) for func in funcs):
                if attr_eq:
                    if all(
                        getattr(update, key) == attr for key, attr in attr_eq.items()
                    ):
                        self.request.app["_dispatcher"].loop.create_task(
                            callback(update)
                        )

                else:
                    self.request.app["_dispatcher"].loop.create_task(callback(update))


def setup(secret_key, dispatcher, app: web.Application, path=None):
    app["_secret_key"] = secret_key
    app["_check_ip"] = _check_ip
    app["_dispatcher"] = dispatcher
    app.router.add_view(
        path or DEFAULT_QIWI_WEBHOOK_PATH,
        BaseWebHookView,
        name=DEFAULT_QIWI_ROUTER_NAME,
    )
