import ipaddress
import typing
import logging

from aiohttp.web import Application

from ..wallet.models import updates
from ..models import utils
from ..requests import deserialize
from ..server import BaseWebHookView
from ..wallet.handler import Handler


logger = logging.getLogger("aioqiwi")

logger.info(f"Deserialization tool: {deserialize.__name__}")

DEFAULT_QIWI_WEBHOOK_PATH = "/webhooks/qiwi/"
DEFAULT_QIWI_ROUTER_NAME = "QIWI"

RESPONSE_TIMEOUT = 55

QIWI_IP_1 = ipaddress.IPv4Address("91.232.231.36")
QIWI_IP_2 = ipaddress.IPv4Address("91.232.231.35")

allowed_ips = {QIWI_IP_1, QIWI_IP_2}

logger.info(f'Default allowed qiwi-addresses are {allowed_ips}')


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


class QiwiWalletWebView(BaseWebHookView):
    _check_ip = _check_ip

    async def parse_update(self) -> updates.QiwiUpdate:
        """
        Deserialize update and create new update class
        :return: :class:`updated.QiwiUpdate`
        """
        data = await self.request.json()
        return utils.json_to_model(deserialize(data), updates.QiwiUpdate)


def setup(dispatcher: Handler, app: Application, path=None):
    app["_check_ip"] = _check_ip
    app["_dispatcher"] = dispatcher
    path = path or DEFAULT_QIWI_WEBHOOK_PATH
    app.router.add_view(
        path,
        QiwiWalletWebView,
        name=DEFAULT_QIWI_ROUTER_NAME,
    )
    logger.info(f'Added view to endpoint {path}')
