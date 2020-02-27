import time
import asyncio
import logging
import datetime
import warnings
from typing import List, Union, Optional

from aiohttp import web

from ..urls import Urls
from ..wallet import enums, server, handler
from ..requests import Requests, serialize
from ..utils.phone import parse_phone
from ..wallet.types import (
    offer,
    stats,
    balance,
    history,
    payment,
    webhook,
    auth_user,
    commission,
    identification,
    phone_provider,
)
from ..utils.requests import get_currency, params_filter, new_http_session
from ..utils.currencies.currency_utils import Currency

try:
    import aiofiles
except ImportError:
    aiofiles = None

_get_loop = asyncio.get_event_loop

logger = logging.getLogger("aioqiwi")
warn = warnings.warn


class Wallet(Requests):
    """
    Qiwi wallet api methods including webhooks
    """

    def __init__(self, api_hash: str, phone_number: Union[str, int] = None, loop=None):
        """
        Main class for requests
        :param api_hash: Qiwi unique token given for an account
        :param phone_number: Bind phone number integer or string
        """
        session = new_http_session(api_hash)

        # http-session and requests shortcuts
        self._session = session
        self._get = session.get
        self._post = session.post
        self._put = session.put
        self._delete = session.delete
        self._patch = session.patch

        self._empty_headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
        }

        if phone_number:
            self._phone_number = parse_phone(phone_number)
        else:
            self._phone_number = None

        self.as_model = True
        self.loop = loop or _get_loop()
        self._handler = handler.Handler(self.loop)

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: Union[str, int]):
        self._phone_number = parse_phone(value)

    def _raise_for_phone(self):
        raise RuntimeWarning(
            "Some methods require setting phone number, instance.phone_number = '+...'"
        )

    # end region

    # getMe region

    async def me(
        self,
        auth_info_enabled: bool = True,
        contract_info_enabled: bool = True,
        user_info_enabled: bool = True,
    ) -> auth_user.AuthUser:
        """
        Get authorization info
        :param user_info_enabled:
        :param contract_info_enabled:
        :param auth_info_enabled:
        :return:
        """
        url = Urls.me

        params = params_filter(
            {
                "authInfoEnabled": auth_info_enabled,
                "contractInfoEnabled": contract_info_enabled,
                "userInfoEnabled": user_info_enabled,
            }
        )

        async with self._get(url, params=params) as response:
            return await self._make_return(response, auth_user.AuthUser)

    # end region

    # identification region
    async def identification(
        self, identification_class: Optional[identification.Identification] = None
    ) -> identification.Identification:
        """
        Get your current identification status, or pass identificationWidget class to request qiwi to verify you
        :param identification_class: convenient class for params storing
        :return: current identification status and request status
        """
        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.identification.format(self.phone_number)

        if not identification_class:
            async with self._get(url) as response:
                return await self._make_return(response, identification.Identification)

        async with self._post(url, json=identification_class.json()) as response:
            return await self._make_return(response, identification.Identification)

    # end region

    # region payment statistics, payment-cheques, history
    async def history(
        self,
        rows: int,
        *,
        operation: enums.PaymentTypes = enums.PaymentTypes.ALL.value,
        sources: list = None,
        from_date: Union[str, datetime.datetime] = None,
        to_date: Union[str, datetime.datetime] = None,
        offset_date: Union[str, datetime.datetime] = None,
        offset_id: int = None,
    ) -> history.History:
        """
        Get payments history from new to old
        :param rows: Quantity of operations
        :param operation: one from <IN, ALL, OUT> see aioqiwi.wallet.enums.enums.PaymentTypes
        :param sources: payment source see aioqiwi.wallet.enums:PaymentSources
        :param from_date: from date strftime with timezone (formatted datetime `YYYY-MM-DDThh:mm:ssTZ`)
        :param to_date: till date
        :param offset_date: offset for previous date [use only with offset_id]
        :param offset_id: offset id for ... [use only with offset_date]
        :return: history.History object
        """

        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.history.format(self.phone_number)
        operation = enums.PaymentTypes(operation).value

        params = params_filter(
            {
                "rows": rows,
                "operation": operation,
                "sources": sources,
                "startDate": self.parse_date(from_date) if from_date else None,
                "endDate": self.parse_date(to_date) if to_date else None,
                "nextTxnDate": self.parse_date(offset_date) if offset_date else None,
                "nextTxnId": offset_id,
            }
        )

        async with self._get(url, params=params) as response:
            return await self._make_return(response, history.History)

    async def stats(
        self,
        *,
        from_date: Union[str, datetime.datetime] = datetime.datetime.now()
        - datetime.timedelta(days=89),
        to_date: Union[str, datetime.datetime] = datetime.datetime.now(),
        operation: enums.PaymentTypes = enums.PaymentTypes.ALL,
        sources: enums.PaymentSources = None,
    ) -> stats.Stats:
        """
        Get statistics of payments
        :param from_date: from date strftime with timezone, pass EasyDate object for convenience or
                str-formatted datetime `YYYY-MM-DDThh:mm:ssZ` - from docs
        :param to_date: like from_date but to
        :param operation: one from <IN, ALL, OUT> see aioqiwi.wallet.enums.enums.PaymentTypes
        :param sources: payment source see aioqiwi.wallet.enums:PaymentSources
        :return: stats object with incoming_total, outgoing_total
        """
        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.stats.format(self.phone_number)

        params = params_filter(
            {
                "operation": operation,
                "sources": sources,
                "startDate": self.parse_date(from_date),
                "endDate": self.parse_date(to_date),
            }
        )

        async with self._get(url, params=params) as response:
            return await self._make_return(response, stats.Stats)

    async def cheque(
        self,
        transaction_id: int,
        transaction_type: str,
        ftype: str,
        destination_dir: str = "aioqiwi_tmp/",
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

        if not all(
            (
                enums.ChequeTypes.has(ftype.upper()),
                enums.PaymentTypes.has(transaction_type.upper()),
            )
        ):
            raise ValueError("Unknown file type or transaction type")

        params = {"type": transaction_type.upper(), "format": ftype.upper()}

        async with self._get(url, params=params) as response:
            destination = f"{destination_dir}/{filename or ('aioqiwi_' + str(transaction_id))}'.{ftype.lower()}"
            binary = await response.read()
            if aiofiles:
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
        _none_model: bool = False,
    ) -> Optional[webhook.WebHookConfig]:
        """
        Register and manage your web-hooks
        :param url: your server endpoint that qiwi will send updates to
        :param transactions_type: 0 => incoming, 1 => outgoing, 2 => all
        :param send_test_notification: qiwi will send you test webhook update
        :param _none_model: new_hooks use it, better do not touch
        :return: Hooks or None
        """
        server_url = url
        url = Urls.Hooks.register

        if not server_url and not transactions_type:
            url = Urls.Hooks.test if send_test_notification else Urls.Hooks.active
            async with self._get(url) as response:
                if not send_test_notification:
                    return await self._make_return(
                        response, webhook.WebHookConfig, force_non_model=_none_model
                    )
                else:
                    raise ValueError("Nothing to fetch/post!")

        params = params_filter(
            {"hookType": 1, "param": server_url, "txnType": transactions_type or 2}
        )

        async with self._put(url, params=params) as response:
            return await self._make_return(
                response, webhook.WebHook, force_non_model=_none_model
            )

    async def delete_hooks(self, hook_id: str = None) -> dict:
        """
        Removes hooks by hook_id if exists
        :param hook_id: active hook_id
        :return: json-response
        """
        if not hook_id:
            hook = await self.hooks()
            hook_id = hook["hookId"] if isinstance(hook, dict) else hook.hook_id

        url = Urls.Hooks.delete.format(hook_id)
        async with self._delete(url) as response:
            return await response.json()

    async def new_hooks(
        self, new_url: str, transactions_types: int = 2
    ) -> webhook.WebHookConfig:
        """
        NON-API EXCLUSIVE method to `reset` your current webhook details
        :param new_url: service url
        :param transactions_types: 0, 1, 2 is 2 by default
        :return: Active Hooks
        """

        active = await self.hooks(_none_model=True)
        if "hookId" in active:
            await self.delete_hooks(active["hookId"])
        else:
            warn(
                "Seems you didn't have registered webhooks. Setting new to %s"
                % new_url,
                RuntimeWarning,
            )

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
        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.Balance.balance.format(self.phone_number)

        if not alias:
            async with self._get(url) as response:
                return await self._make_return(response, balance.Balance)

        url = Urls.Balance.set_new_balance.format(self.phone_number, alias)

        async with self._patch(url, data={"defaultAccount": True}) as response:
            return await response.json()

    async def available_balances(self) -> List[offer.Offer]:
        """
        Get aliases of available offers
        :return: list[Offer]
        """
        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.Balance.available_aliases

        async with self._get(url) as response:
            return await self._make_return(response, offer.Offer)

    # end region

    # payments region
    async def transaction(
        self,
        provider_id: int,
        payment_type: Union[
            payment.BankPayment,
            payment.CellTopUp,
            payment.CardPayment,
            payment.P2PPayment,
        ],
    ) -> payment.Payment:
        """
        :return: Payment (completed)
        """
        url = Urls.Payments.base.format(provider_id)

        if not payment_type.id:
            payment_type.id = str(time.time() * 1000)

        async with self._post(url, data=payment_type.json()) as response:
            return await self._make_return(response, payment.Payment)

    async def commission(
        self,
        amount: float,
        receiver: Union[str, int],
        provider: Union[enums.Provider] = enums.Provider.QIWI_WALLET.value,
        *,
        currency: Union[Currency, str, int] = Currency["643"].isoformat,
    ) -> commission.Commission:
        """
        Get commission info for a transaction
        :param amount: amount of money theoretically will be sent
        :param receiver: receiver
        :param provider: provider id default is qiwi
        :param currency: ISO of currency DEFAULT and the only acceptable(from qiwidocs) is 643 ruble
        :return:
        """
        url = Urls.Payments.commission.format(enums.Provider(provider).value)

        currency = get_currency(currency).isoformat
        data = serialize(
            {
                "account": parse_phone(receiver),
                "paymentMethod": {"type": "Account", "accountId": currency},
                "purchaseTotals": {"total": {"amount": amount, "currency": currency}},
            }
        )

        async with self._post(url, data=data) as response:
            return await self._make_return(response, commission.Commission)

    async def detect_provider(
        self, phone: Union[str, int] = None
    ) -> phone_provider.Provider:
        """
        Helper for getting phone number's enums.Provider id
        :param phone: pass phone number or
                      it will try to get passed phone_number in initialization otherwise ask you to enter
        :return: Provider object
        """
        if not phone and not self.phone_number:
            self._raise_for_phone()

        url = Urls.Payments.providers
        params = params_filter({"phone": phone or self.phone_number})

        headers = {
            "Accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
        }

        async with self._get(url, params=params, headers=headers) as response:
            return await self._make_return(response, phone_provider.Provider)

    # end region

    # blocking op setup -> run server
    def idle(
        self,
        host: str = "localhost",
        port: int = 7494,
        path: str = None,
        app: web.Application = None,
    ):
        """
        :param host: server host
        :param port: server port that open for tcp/ip trans.
        :param path: path for qiwi that will send requests
        :param app: pass web.Application if you want, common-use - aiogram powered webhook-bots
        """
        app = app or web.Application()
        server.setup(self._handler, app, path)

        web.run_app(app, host=host, port=port)

    def configure_for_app(self, app, path=None):
        """
        If you want to implement your start_webhook execution use this method and get configured listener with
        configured web-view for passed path[see default in webhooks/server.py]
        :param app: aiohttp.web.Application initialized
        :param path: url path
        """
        server.setup(self._handler, app, path)

    # end region

    # session-related
    async def close(self):
        await self._session.close()

    # updates handler
    @property
    def on_update(self):
        return self._handler.payment_event
