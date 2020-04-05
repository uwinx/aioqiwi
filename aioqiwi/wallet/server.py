import ipaddress

from aiohttp.web import Application

from ..core import handler, server
from ..wallet.types import webhook

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


class QiwiWalletWebView(server.BaseWebHookView):
    def _check_ip(self, ip: str):
        return _check_ip(ip)

    async def parse_update(self) -> webhook.WebHook:
        """
        Deserialize update and create new update class
        :return: :class:`updated.QiwiUpdate`
        """
        data = await self.request.read()
        return webhook.WebHook(**self.json_module.deserialize(data))

    app_key_check_ip = "_qiwi_wallet_check_ip"
    app_key_handler_manager = "_qiwi_wallet_handler_manager"


def setup(handler_manager: handler.HandlerManager, app: Application, path: str = None):
    app[QiwiWalletWebView.app_key_check_ip] = _check_ip
    app[QiwiWalletWebView.app_key_handler_manager] = handler_manager
    path = path or DEFAULT_QIWI_WEBHOOK_PATH
    app.router.add_view(path, QiwiWalletWebView, name=DEFAULT_QIWI_ROUTER_NAME)
