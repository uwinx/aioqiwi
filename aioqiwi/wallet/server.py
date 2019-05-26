import ipaddress
import typing
import logging

from aiohttp.web import View, Response, Application, HTTPUnauthorized

from ..wallet.models import updates
from ..models import utils
from ..mixin import deserialize
from ..wallet.handler import Handler


logger = logging.getLogger("aioqiwi")

logger.info(f"Deserialization tool: {deserialize.__name__}")

DEFAULT_QIWI_WEBHOOK_PATH = "/webhooks/qiwi/"
DEFAULT_QIWI_ROUTER_NAME = "QIWI"

RESPONSE_TIMEOUT = 55

QIWI_IP_1 = ipaddress.IPv4Address("91.232.231.36")
QIWI_IP_2 = ipaddress.IPv4Address("91.232.231.35")

allowed_ips = {QIWI_IP_1, QIWI_IP_2}


def _check_ip(ip: str) -> bool:
    """
    Check if ip is allowed to request us
    :param ip: IP-address
    :return: address is allowed
    """
    address = ipaddress.IPv4Address(ip)
    return address in allowed_ips


def allow_ip(*ips: typing.Union[str, ipaddress.IPv4Network, ipaddress.IPv4Address]):
    """
    Add new ips to allowed
    """
    for ip in ips:
        if isinstance(ip, ipaddress.IPv4Address):
            allowed_ips.add(ip)
        elif isinstance(ip, str):
            allowed_ips.add(ipaddress.IPv4Address(ip))
        elif isinstance(ip, ipaddress.IPv4Network):
            allowed_ips.update(ip.hosts())
        else:
            raise ValueError


class BaseWebHookView(View):
    def validate_ip(self):
        # pulled from aiogram.dispatcher.webhook validator big thanks
        if self.request.app.get("_check_ip", False):
            ip_address, accept = self.check_ip()
            if not accept:
                raise HTTPUnauthorized()

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
        """
        Process GET
        :return:
        """
        self.validate_ip()
        return Response(text="up")

    async def post(self):
        """
        Process POST request with validating, further deserialization and resolving
        :return: :class:``
        """
        self.validate_ip()

        update = await self.parse_update()
        await self._resolve_update(update)

        return Response(text="ok", status=200)

    async def parse_update(self):
        """
        Deserialize update and create new update class
        :return: :class:`updated.QiwiUpdate`
        """
        data = await self.request.json()
        return utils.json_to_model(deserialize(data), updates.QiwiUpdate)

    async def _resolve_update(self, update: updates.QiwiUpdate):
        for callback, funcs, attr_eq in self.request.app["_dispatcher"].handlers:
            if all(func(update) for func in funcs):
                if attr_eq:
                    if all(
                        [getattr(update, key) == attr for key, attr in attr_eq.items()]
                    ):
                        self.request.app["_dispatcher"].loop.create_task(
                            callback(update)
                        )

                else:
                    self.request.app["_dispatcher"].loop.create_task(callback(update))


def setup(dispatcher: Handler, app: Application, path=None):
    app["_check_ip"] = _check_ip
    app["_dispatcher"] = dispatcher
    app.router.add_view(
        path or DEFAULT_QIWI_WEBHOOK_PATH,
        BaseWebHookView,
        name=DEFAULT_QIWI_ROUTER_NAME,
    )
