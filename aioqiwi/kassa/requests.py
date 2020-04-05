import asyncio
import base64
import datetime
import logging
import uuid
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from ..core import currencies, handler
from ..core.requests import Requests
from ..core.tooling import phone as phone_module
from .server import setup
from .types import invoice, refund
from .urls import urls

if TYPE_CHECKING:
    from aiohttp import web

logger = logging.getLogger("aioqiwi")


class QiwiKassa(Requests):
    def __init__(
        self,
        api_hash: str,
        timeout: Optional[Union[float, int]] = None,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        event_process_strategy: Optional[handler.EventProcessStrategy] = None,
    ):
        """
        Beta of kassa.qiwi.com currently developing
        :param api_hash: Qiwi unique token given for an account
        """
        super().__init__(api_hash, timeout, event_loop=loop)

        self.__api_hash = api_hash

        self.handler_manager = handler.HandlerManager(self.loop, event_process_strategy)

    @classmethod
    def _get_currency_code(
        cls, currency: Optional[Union[str, int, currencies.CurrencyModel]] = None
    ) -> str:
        if isinstance(currency, (str, int)):
            temp = currencies.Currency.get(currency)
            if temp is None:
                raise ValueError(f"Could not find loaded Currency for {currency!s}")
            return temp.code
        elif isinstance(currency, currencies.CurrencyModel):
            return currency.code
        else:
            raise TypeError(
                f"Invalid type got for currency code,"
                f"expected {(str, int, currencies.CurrencyModel)!r},"
                f" got {currency!r}"
            )

    @classmethod
    def generate_bill_id(cls):
        """
        Generates unique bill_id
        However you can implement your generator :idk:
        """
        return (
            base64.urlsafe_b64encode(uuid.uuid3(uuid.uuid4(), "").bytes)
            .decode()
            .rstrip("=")
            .upper()
        )

    async def new_bill(
        self,
        amount: float,
        peer_phone: Optional[Union[str, int]] = None,
        peer_email: Optional[str] = None,
        lifetime: Union[int, datetime.datetime] = 10,
        *,
        currency: Union[str, int, currencies.CurrencyModel] = "643",
        comment: str = "q> aioqiwi <p",
        bill_id: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> invoice.Invoice:
        """
        Create new bill
        :param amount: invoice amount rounded down to two decimals
        :param peer_phone: phone number to which invoice issued
        :param peer_email: client's e-mail
        :param lifetime: invoice due date pass int for `days` representation
        :param currency: pass currencies.Currency object or integer code like <845> of currency or str code like <'USD'>
        :param comment: invoice commentary
        :param bill_id: unique invoice identifier in merchant's system
        :param custom_fields
        :return: Invoice if success
        """
        url = urls.bill.format(bill_id or self.generate_bill_id())

        if isinstance(lifetime, int):
            lifetime = datetime.datetime.now() + datetime.timedelta(days=lifetime)

        data = self._tools.json_module.serialize(
            {
                "amount": {
                    "currency": self._get_currency_code(currency),
                    "value": amount,
                },
                "comment": comment,
                "expirationDateTime": self._tools.datetime_module.check_and_parse_datetime(
                    lifetime
                ),
                "customer": {
                    "phone": phone_module.parse_phone(peer_phone),
                    "account": peer_email,
                }
                if peer_phone and peer_email
                else {},
                "customFields": custom_fields or {},
            }
        )

        response = await self.connector.request("PUT", url, data=data)
        return await self._make_return(response, invoice.Invoice)

    async def bill_info(self, bill_id: str) -> invoice.Invoice:
        """
        Get info about bill
        :param bill_id: bill's id in your system
        :return: kassa.models.Invoice instance
        """
        url = urls.bill.format(bill_id)

        response = await self.connector.request("GET", url)
        return await self._make_return(response, invoice.Invoice)

    async def reject_bill(self, bill_id: str) -> invoice.Invoice:
        """
        Reject bill
        :param bill_id: bill's id in your system
        :return: kassa.models.Invoice
        """
        url = urls.reject.format(bill_id)

        response = await self.connector.request("POST", url)
        return await self._make_return(response, invoice.Invoice)

    async def refund(
        self,
        bill_id: str,
        refund_id: str,
        amount: Optional[float] = None,
        currency: Optional[Union[str, int]] = None,
    ) -> refund.Refund:
        """
        Refund user's money, pass amount and currency to refund, else will get info about refund
        :param bill_id: bill's id in your system
        :param refund_id: refund id
        :param amount: amount to refund
        :param currency: currency
        :return: Refund class instance
        """
        url = urls.refund.format(bill_id, refund_id)

        if not amount and not currency:
            response = await self.connector.request("GET", url)
            return await self._make_return(response, refund.Refund)

        data = self._tools.json_module.serialize(
            {"amount": {"currency": self._get_currency_code(currency), "value": amount}}
        )

        response = await self.connector.request("PUT", url, data=data)
        return await self._make_return(response, refund.Refund)

    def configure_listener(
        self,
        app: "web.Application",
        path: Optional[str] = None,
        close_connector_ate: bool = True,
    ):
        """
        Pass aiohttp.web.Application and aioqiwi.kassa.server will bind itself to your app
        :param close_connector_ate:
        :param app: existing aiohttp application
        :param path: your endpoint, see default in aioqiwi.kassa.server.py
        :return:
        """

        if close_connector_ate:
            app.on_shutdown.append(self._on_app_shutdown)

        setup(self.__api_hash, self.handler_manager, app, path=path)

    def idle(
        self,
        host: str = "localhost",
        port: int = 7494,
        path: Optional[str] = None,
        app: "Optional['web.Application']" = None,
        close_connector_ate: bool = True,
    ):
        """
        [WARNING] This is blocking io method
        :param close_connector_ate:
        :param host: server host
        :param port: server port that open for tcp/ip trans.
        :param path: path for qiwi that will send requests
        :param app: pass aiohttp web application
        """
        from aiohttp import web

        app = app if app is not None else web.Application()

        if close_connector_ate:
            app.on_shutdown.append(self._on_app_shutdown)

        setup(self.__api_hash, self.handler_manager, app or web.Application(), path)
        web.run_app(app, host=host, port=port)

    async def _on_app_shutdown(self, _):
        await self.close()
