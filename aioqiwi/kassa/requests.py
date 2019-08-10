import asyncio
import base64
import datetime
import logging
import typing
import uuid

from aiohttp import web

from .handler import Handler
from .models import sent_invoice, refund
from .server import setup
from ..requests import Requests, serialize
from ..urls import Urls
from ..utils.currencies.currency_utils import Currency
from ..utils.phone import parse_phone
from ..utils.requests import new_http_session, get_currency

logger = logging.getLogger("aioqiwi")
loop = asyncio.get_event_loop()  # noqa


class QiwiKassa(Requests):
    def __init__(self, api_hash: str):
        """
        Beta of kassa.qiwi.com currently developing
        :param api_hash: Qiwi unique token given for an account
        """
        session = new_http_session(api_hash)
        self._session = session

        self.__api_hash = api_hash

        self._get = session.get
        self._post = session.post
        self._put = session.put
        self._delete = session.delete
        self._patch = session.patch

        self.loop = loop
        self._handler = Handler(self.loop)

    @staticmethod
    def generate_bill_id():
        """
        Generates unique bill_id
        However you can implement your generator :idk:
        """
        return base64.urlsafe_b64encode(uuid.uuid3(uuid.uuid4(), "").bytes).decode().rstrip("=").upper()

    async def new_bill(
            self,
            amount: float,
            peer: typing.Union[str, int] = None,
            peer_email: str = None,
            lifetime: typing.Union[int, datetime.datetime] = 10,
            *,
            currency: typing.Union[str, int, Currency] = Currency["643"],
            comment: str = "aioqiwi-check",
            bill_id: str = None,
            custom_fields: dict = None
    ) -> sent_invoice.Invoice:
        """
        Create new bill
        :param amount: invoice amount rounded down to two decimals
        :param peer: phone number to which invoice issued
        :param peer_email: client's e-mail
        :param lifetime: invoice due date pass int for `days` representation
        :param currency: pass Currency object or integer code like <845> of currency or str code like <'USD'>
        :param comment: invoice commentary
        :param bill_id: unique invoice identifier in merchant's system
        :param custom_fields
        :return: SentInvoice if success
        """
        url = Urls.P2PBillPayments.bill.format(bill_id or self.generate_bill_id())

        if isinstance(lifetime, int):
            lifetime = datetime.datetime.now() + datetime.timedelta(days=lifetime)

        data = serialize(
            {
                "amount":             {"currency": get_currency(currency).code, "value": amount},
                "comment":            comment,
                "expirationDateTime": self.parse_date(lifetime),
                "customer":           {"phone": parse_phone(peer), "account": peer_email}
                                      if peer and peer_email
                                      else {},
                "customFields":       custom_fields or {},
            }
        )

        async with self._put(data=data, url=url) as response:
            return await self._make_return(response, sent_invoice.Invoice)

    async def bill_info(self, bill_id: str) -> sent_invoice.Invoice:
        """
        Get info about bill
        :param bill_id: bill's id in your system
        :return: kassa.models.Invoice instance
        """
        url = Urls.P2PBillPayments.bill.format(bill_id)

        async with self._get(url) as response:
            return await self._make_return(response, sent_invoice.Invoice)

    async def reject_bill(self, bill_id: str):
        """
        Reject bill
        :param bill_id: bill's id in your system
        :return: kassa.models.Invoice
        """
        url = Urls.P2PBillPayments.reject.format(bill_id)

        async with self._post(url) as response:
            return await self._make_return(response, sent_invoice.Invoice)

    async def refund(
            self,
            bill_id: str,
            refund_id: str,
            amount: float = None,
            currency: typing.Union[str, int] = None,
    ) -> refund.Refund:
        """
        Refund user's money, pass amount and currency to refund, else will get info about refund
        :param bill_id: bill's id in your system
        :param refund_id: refund id
        :param amount: amount to refund
        :param currency: currency
        :return: Refund class instance
        """
        url = Urls.P2PBillPayments.refund.format(bill_id, refund_id)

        if not amount and not currency:
            async with self._get(url) as response:
                return await self._make_return(response, refund.Refund)

        data = serialize(
            {"amount": {"currency": get_currency(currency).code, "value": amount}}
        )

        async with self._put(url, data=data) as response:
            return await self._make_return(response, refund.Refund)

    def on_update(self) -> Handler.update:
        """
        Return function, use it as a decorator
        :return:
        """
        return self._handler.update

    def configure_listener(self, app, path=None):
        """
        Pass aiohttp.web.Application and aioqiwi.kassa.server will bind itself to your app
        :param app:
        :param path: your endpoint, see default in aioqiwi.kassa.server.py:L~:start:
        :return:
        """
        setup(self.__api_hash, self._handler, app, path=path)

    def idle(self, host="localhost", port=7494, path=None, app=None):
        """
        [WARNING] This is blocking io method
        :param host: server host
        :param port: server port that open for tcp/ip trans.
        :param path: path for qiwi that will send requests
        :param app: pass web.Application if you want, common-use - aiogram powered webhook-bots
        :return:
        """
        setup(self._handler, app or web.Application(), path)
        web.run_app(app, host=host, port=port)

    # session-related
    async def close(self):
        await self._session.close()
