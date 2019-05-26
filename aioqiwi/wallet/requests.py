# todo: error handling
import sys
import asyncio
import logging
import typing
import inspect

from aiohttp import client, web

from ..urls import Urls
from ..wallet.models import (
    webhooks,
    balance,
    phone_provider,
    auth_user,
    offer,
    payment,
    identification,
    history,
    stats,
)
from ..models import utils
from ..utils.time_utils import EasyDate, TimeRange
from ..utils.phone import parse_phone
from ..utils.currency_utils import Currency
from ..wallet import handler, server
from ..wallet.helper import Provider, ChequeTypes, PaymentTypes, IdentificationWidget
from ..mixin import serialize, QiwiMixin

AIOFILES = False

try:
    import aiofiles

    AIOFILES = True
except ImportError:
    pass

_get_loop = asyncio.get_event_loop

logger = logging.getLogger("aioqiwi")


class Wallet(QiwiMixin):
    def __init__(self, api_hash: str, phone_number: str or int = None, loop=None):
        """
        Main class for requests
        :param api_hash: Qiwi unique token given for an account
        :param phone_number: Bind phone number integer or string
        """
        session = self._new_http_session(api_hash)

        self.__session = session
        self.__get = session.get
        self.__post = session.post
        self.__put = session.put
        self.__delete = session.delete
        self.__patch = session.patch

        if phone_number:
            self.phone_number = parse_phone(phone_number)
        else:
            self.phone_number = None

        self.as_model = True
        self.__loop = loop or _get_loop()
        self.__handler = handler.Handler(self.__loop)

    async def __check_phone(
        self, prompt: str = "Phone-related method requested, enter phone number first: "
    ):
        """
        Check if developer entered phone for initialized class :xcl:
        :param prompt:
        :return:
        """

        if not self.phone_number:
            try:
                print(prompt, end="")
                self.phone_number = parse_phone(
                    (
                        await self.__loop.run_in_executor(None, sys.stdin.readline)
                    ).rstrip()
                )
            except ValueError:
                await self.__check_phone("Enter correctly: ")

    # end region

    # getMe region
    async def me(self, params: dict or auth_user.Me = None) -> auth_user.AuthUser:
        """
        Get authorization info
        :param params:
        :return:
        """
        url = Urls.me

        if isinstance(params, auth_user.Me):
            params = params.dict_params()

        async with self.__get(url, params=params) as response:
            return await self._make_return(response, auth_user.AuthUser)

    # end region

    # identification region
    async def identification(
        self, identification_class: IdentificationWidget = None
    ) -> identification.Identification:
        """
        Get your current identification status, or pass identificationWidget class to request qiwi to verify you
        :param identification_class: convenient class for params storing
        :return: current identification status and request status
        """
        await self.__check_phone()

        url = Urls.identification.format(self.phone_number)

        if not identification_class:
            async with self.__get(url) as response:
                return await self._make_return(response, identification.Identification)

        async with self.__post(url, json=identification_class.as_dict()) as response:
            return await self._make_return(response, identification.Identification)

    # end region

    # region payment statistics and history
    async def history(
        self,
        rows: int,
        *,
        operation: str = "ALL",
        sources: list = None,
        from_date: str or EasyDate = None,
        to_date: str or EasyDate = None,
        timerange: TimeRange = None,
        offset_date: str or EasyDate = None,
        offset_id: int = None,
    ) -> history.HistoryList:
        """
        Get payments history from new to old
        :param rows: Quantity of operations
        :param operation: one from <IN, ALL, OUT> see aioqiwi.wallet.helper.PaymentTypes
        :param sources: payment source see aioqiwi.wallet.helper:PaymentSources
        :param from_date: from date strftime with timezone, pass EasyDate object for convenience or
                str-formatted datetime `YYYY-MM-DDThh:mm:ssZ` - from docs
        :param to_date: like from_date but to
        :param timerange: exclusive argument, pass TimeRange object
        :param offset_date: offset for previous date [use only with offset_id]
        :param offset_id: offset id for ... [use only with offset_date]
        :return: history.History object
        """

        await self.__check_phone()

        url = Urls.history.format(self.phone_number)

        if timerange:
            from_date, to_date = timerange.dates

        params = self._param_filter(
            {
                "rows": rows,
                "operation": operation,
                "sources": sources,
                "startDate": str(from_date) if from_date else None,
                "endDate": str(to_date) if to_date else None,
                "nextTxnDate": str(offset_date) if offset_date else None,
                "nextTxnId": offset_id,
            }
        )

        async with self.__get(url, params=params) as response:
            return await self._make_return(
                response, history.HistoryList, history.History
            )

    async def stats(
        self,
        *,
        from_date: str or EasyDate = EasyDate().go_back(89),
        to_date: str or EasyDate = EasyDate(),
        operation: str = "ALL",
        sources: list = None,
        timerange: TimeRange = None,
    ) -> stats.Stats:
        """
        Get statistics of payments
        :param from_date: from date strftime with timezone, pass EasyDate object for convenience or
                str-formatted datetime `YYYY-MM-DDThh:mm:ssZ` - from docs
        :param to_date: like from_date but to
        :param operation: one from <IN, ALL, OUT> see aioqiwi.wallet.helper.PaymentTypes
        :param sources: payment source see aioqiwi.wallet.helper:PaymentSources
        :param timerange: exclusive, pass TimeRange object
        :return: stats object with incoming_total, outgoing_total
        """

        await self.__check_phone()
        url = Urls.stats.format(self.phone_number)

        if timerange:
            from_date, to_date = timerange.dates

        params = self._param_filter(
            {
                "operation": operation,
                "sources": sources,
                "startDate": str(from_date),
                "endDate": str(to_date),
            }
        )

        async with self.__get(url, params=params) as response:
            return await self._make_return(response, stats.Stats, stats.Payment)

    async def cheque(
        self,
        transaction_id: int,
        transaction_type: str,
        ftype: str,
        destination_dir: str = ".",
        filename: str = None,
    ) -> str:
        """
        Get cheque for transaction available types: JPEG, PDF
        :param transaction_id: tnxId from history object
        :param transaction_type: incoming or outgoing
        :param ftype: return file type JPEG or PDF
        :param destination_dir: path to save
        :param filename: filename to save
        """
        url = Urls.cheque.format(transaction_id)

        if ftype.upper() not in ChequeTypes or transaction_type.upper() not in [
            PaymentTypes.IN,
            PaymentTypes.OUT,
        ]:
            raise ValueError("Unknown file type or transaction type")

        params = {"type": transaction_type.upper(), "format": ftype.upper()}

        async with self.__get(url, params=params) as response:
            destination = (
                f"{destination_dir}/{filename or transaction_id}.{ftype.lower()}"
            )
            binary = await response.read()
            if AIOFILES:
                async with aiofiles.open(destination, "wb") as fp:
                    await fp.write(binary)
            else:
                with open(destination, "wb") as fp:
                    fp.write(binary)
            return destination

    # end region

    # region web-hooks
    async def hooks(
        self,
        url: str = None,
        transactions_type: int = None,
        *,
        send_test_notification: bool = False,
    ) -> webhooks.Hooks:
        """
        Register and manage your web-hooks
        >>> async def main():
        ...     async with Wallet('api_hash', '743987937') as client:
        ...         # Register new web-hook
        ...         info = await client.hooks('mysite.domain/webhooks-for-qiwi/')
        ...         info.hook_id  #-> 'f14vrgb88s6a90211m6v6espg9shi9ah9tbug9ayv9nema'
        ...         # Get active webhook information
        ...         info = await client.hooks()  # get active web-hook information
        ...         info.hook_id  #-> 'f14vrgb88s6a90211m6v6espg9shi9ah9tbug9ayv9nema'
        ...         # Ask qiwi to send test webhook
        ...         await client.hooks(send_test_notification=True)

        :param url: your server endpoint that qiwi will send updates to
        :param transactions_type: 0 => incoming, 1 => outgoing, 2 => all
        :param send_test_notification: qiwi will send you test webhook update
        :return: Hooks or None
        """
        server_url = url
        url = Urls.Hooks.register

        if not server_url and not transactions_type:
            url = Urls.Hooks.test if send_test_notification else Urls.Hooks.active
            async with self.__get(url) as response:
                if not send_test_notification:
                    return await self._make_return(response, webhooks.Hooks)
                else:
                    raise ValueError("Nothing will be done!")

        params = {"hookType": 1, "param": server_url, "txnType": transactions_type or 2}

        async with self.__put(url, params=params) as response:
            resp = await response.json()
            return utils.json_to_model(resp, webhooks.Hooks) if self.as_model else resp

    async def delete_hooks(self, hook_id: str = None) -> dict:
        """
        Removes hooks by hook_id if exists
        :param hook_id: active hook_id
        :return: json-response
        """
        if not hook_id:
            hook_id = (await self.hooks()).hook_id

        url = Urls.Hooks.delete.format(hook_id)
        async with self.__delete(url) as response:
            return await response.json()

    async def new_hooks(
        self, new_url: str, transactions_types: int = 2
    ) -> webhooks.Hooks:
        """
        NON-API EXCLUSIVE method to `reset` your current webhook details
        :param new_url: service url
        :param transactions_types: 0, 1, 2 is 2 by default
        :return: Active Hooks
        """
        active = await self.hooks(None, None)
        if not active:
            raise ValueError("You do not have active webhooks")

        await self.delete_hooks(active.hook_id)
        return await self.hooks(new_url, transactions_types)
    # end region

    # balance related region
    async def balance(self, alias: str = None) -> balance.Balance:
        """
        Get your current "WALLETS" aka balances for particular currency
        Pass alias if you want to change default balance
        :param alias: alias from `*.available_balances().alias`
        :return: balance.Balance object
        """
        await self.__check_phone()
        url = Urls.Balance.balance.format(self.phone_number)

        if not alias:
            async with self.__get(url) as response:
                return await self._make_return(
                    response, balance.Balance, balance.Account
                )

        url = Urls.Balance.set_new_balance.format(self.phone_number, alias)

        async with self.__patch(url, data={"defaultAccount": True}) as response:
            return await response.json()

    async def available_balances(self) -> typing.List[offer.Offer]:
        """
        Get aliases of available offers
        :return: list[Offer]
        """
        await self.__check_phone()
        url = Urls.Balance.available_aliases

        async with self.__get(url) as response:
            return await self._make_return(response, offer.Offer, spec_ignore=True)

    # end region

    async def transaction(
        self,
        amount: float or int,
        receiver: str or int,
        currency: str or int or Currency = '648',
        provider_id: int = Provider.QIWI_WALLET,
        comment: str = "via aioqiwi",
        fields: dict = None,
    ) -> payment.Payment:
        """
        |Make base transaction| sends to qiwi wallet by default [WARNING] if you are not sure about param-passing
        please wait till I implement helpful methods for that changes `*.transaction` behaviour for the particular
        situation
        :param amount: amount of money will be sent
        :param receiver: phone number/bank account number/
        :param currency: 648 ISO by default change it if you want [better do not touch]
        :param provider_id: QIWI by default do not change if you are not sure use other method *_transaction
        :param comment: text for comment
        :param fields: do not pass !payments.FieldsWidget! use other method *_transaction
        :return: Payment (completed)
        """
        url = Urls.Payments.base.format(provider_id)

        ccode = self.get_currency(currency)
        data = serialize(
            self._param_filter(
                {
                    "id": EasyDate().datetime.utcnow().timestamp().__int__().__str__(),
                    "sum": {"amount": round(float(amount), 2), "currency": ccode},
                    "paymentMethod": {"type": "Account", "accountId": ccode},
                    "fields": fields or {"account": parse_phone(receiver)},
                    "comment": comment,
                }
            )
        )

        async with self.__post(url, data=data) as response:
            return await self._make_return(response, payment.Payment)

    async def detect_provider(
        self, phone: str or int = None
    ) -> phone_provider.Provider:
        """
        Helper for getting phone number's provider id
        :param phone: pass phone number or
                      it will try to get passed phone_number in initialization otherwise ask you to enter
        :return: Provider object
        """
        url = Urls.providers
        params = self._param_filter(
            {
                "phone": self.phone_number or await self.__check_phone()
                if not phone
                else parse_phone(phone)
            }
        )

        headers = {
            "Accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
        }

        async with self.__get(url, params=params, headers=headers) as response:
            return await self._make_return(response, phone_provider.Provider)

    # blocking op
    def idle(self, *blocking_funcs, host="localhost", port=6969, path=None, app=None):
        """
        [WARNING] This is blocking io method
        :params blocking_funcs: pass any func and it'll we executed async-ly with run-app
        PASSING RULE: [FUNC, *ARGS, **KWARGS]
        :param host: server host
        :param port: server port that open for tcp/ip trans.
        :param path: path for qiwi that will send requests
        :param app: pass web.Application if you want, common-use - aiogram powered webhook-bots
        :return:
        """

        async def inner_tsk(func, args_, kwargs_):
            if inspect.iscoroutine(func):
                await func(*args_, **kwargs_)
            func(*args_, **kwargs_)

        if isinstance(blocking_funcs, (list, tuple, set)):
            for item in blocking_funcs:
                args = item[1] if len(item) >= 2 else []
                kwargs = (
                    item[2]
                    if len(item) == 3
                    else item[1]
                    if len(item) >= 2 and isinstance(item[1], dict)
                    else {}
                )
                self.__loop.create_task(inner_tsk(item[0], args, kwargs))

        server.setup(self.__handler, app or web.Application(), path)
        web.run_app(app, host=host, port=port)

    def configure_for_app(self, app, path=None):
        """
        If you want to implement your start_webhook execution use this method and get configured listener with
        configured web-view for passed path[see default in webhooks/server.py]
        :param app: aiohttp.web.Application initialized
        :param path:
        """
        server.setup(self.__handler, app, path)

    # updates handler
    @property
    def on(self):
        return self.__handler

    async def close(self):
        await self.__session.close()

    # `async with` block
    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


class _Payments:
    # TODO
    # some monkey-patch tools for QiwiAccount.transaction method
    # Here we'll be super-easy-to-use methods, idk now
    def __init__(self, send_function: Wallet.transaction):
        self.send: Wallet.transaction = send_function
