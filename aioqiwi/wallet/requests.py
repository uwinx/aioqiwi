import datetime
import logging
import time
import warnings
from typing import List, Optional, Union

from aiohttp import web

from ..core import currencies, handler
from ..core import phone as phone_module
from ..core import requests, returns
from ..urls import Urls
from ..wallet import enums, server
from ..wallet.types import (
    auth_user,
    balance,
    commission,
    history,
    identification,
    offer,
    payment,
    phone_provider,
    stats,
    webhook,
)

try:
    import aiofiles
except ImportError:
    aiofiles = None

logger = logging.getLogger("aioqiwi")


class Wallet(requests.Requests):
    """
    Qiwi wallet api methods including webhooks
    """

    def __init__(
        self,
        api_hash: str,
        phone_number: Optional[Union[str, int]] = None,
        loop=None,
        event_process_strategy: handler.EventProcessStrategy = None,
    ):
        """
        Main class for requests
        :param api_hash: Qiwi unique token given for an account
        :param phone_number: Bind phone number integer or string
        """
        super().__init__(api_hash, event_loop=loop)

        if phone_number:
            self._phone_number = phone_module.parse_phone(phone_number)
        else:
            self._phone_number = None

        self.handler_manager = handler.HandlerManager(self.loop, event_process_strategy)

    @property
    def phone_number(self):
        return self._phone_number

    @phone_number.setter
    def phone_number(self, value: Union[str, int]):
        self._phone_number = phone_module.parse_phone(value)

    def _raise_for_phone(self, _has_invalid_format=False):
        raise RuntimeWarning(
            "Phone number could not be recognised. Please enter set it correctly."
            if _has_invalid_format
            else "Some methods require setting phone number, instance.phone_number = '+...'"
        )

    # end region

    # currency region
    @classmethod
    def _get_currency_isoformat(
        cls, currency: Optional[Union[currencies.CurrencyModel, str, int]]
    ) -> Optional[str]:
        if isinstance(currency, (str, int)):
            temp = currencies.Currency.get(currency)
            if temp is None:
                raise ValueError(f"Could not find loaded Currency for {currency!s}")
            return temp.isoformat
        elif isinstance(currency, currencies.CurrencyModel):
            return currency.isoformat
        else:
            raise TypeError(
                f"Invalid type got for currency isoformat,"
                f"expected {(str, int, currencies.CurrencyModel)!r},"
                f" got {currency!r}"
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

        params = self.params_filter(
            {
                "authInfoEnabled": auth_info_enabled,
                "contractInfoEnabled": contract_info_enabled,
                "userInfoEnabled": user_info_enabled,
            }
        )

        async with self._session.get(url, params=params) as response:
            return await self.make_return(
                response=response, current_model=auth_user.AuthUser
            )

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
            async with self._session.get(url) as response:
                return await self.make_return(response, identification.Identification)

        async with self._session.post(
            url, json=identification_class.json()
        ) as response:
            return await self.make_return(response, identification.Identification)

    # end region

    # region payment statistics, payment-cheques, history
    async def history(
        self,
        rows: int,
        *,
        operation: enums.PaymentTypes = enums.PaymentTypes.ALL,
        sources: Optional[List[enums.PaymentSources]] = None,
        from_date: Optional[Union[str, datetime.datetime]] = None,
        to_date: Optional[Union[str, datetime.datetime]] = None,
        offset_date: Optional[Union[str, datetime.datetime]] = None,
        offset_id: Optional[int] = None,
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

        params = self.params_filter(
            {
                "rows": rows,
                "operation": operation,
                "sources": sources,
                "startDate": self.datetime_module.check_and_parse_datetime(from_date),
                "endDate": self.datetime_module.check_and_parse_datetime(to_date),
                "nextTxnDate": self.datetime_module.check_and_parse_datetime(
                    offset_date
                ),
                "nextTxnId": offset_id,
            }
        )

        async with self._session.get(url, params=params) as response:
            return await self.make_return(response, history.History)

    async def stats(
        self,
        *,
        from_date: Union[str, datetime.datetime] = datetime.datetime.now()
        - datetime.timedelta(days=89),
        to_date: Union[str, datetime.datetime] = datetime.datetime.now(),
        operation: enums.PaymentTypes = enums.PaymentTypes.ALL,
        sources: Optional[enums.PaymentSources] = None,
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

        params = self.params_filter(
            {
                "operation": operation,
                "sources": sources,
                "startDate": self.datetime_module.check_and_parse_datetime(from_date),
                "endDate": self.datetime_module.check_and_parse_datetime(to_date),
            }
        )

        async with self._session.get(url, params=params) as response:
            return await self.make_return(response, stats.Stats)

    async def cheque(
        self,
        transaction_id: int,
        transaction_type: str,
        ftype: str,
        destination_dir: str = "aioqiwi_tmp/",
        filename: Optional[str] = None,
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

        params = {
            "type": enums.PaymentTypes(transaction_type.upper()),
            "format": enums.ChequeTypes(ftype.upper()),
        }

        async with self._session.get(url, params=params) as response:
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
        url: Optional[str] = None,
        transactions_type: Optional[int] = None,
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
            async with self._session.get(url) as response:
                if not send_test_notification:
                    return await self.make_return(
                        response,
                        webhook.WebHookConfig,
                        forces_return_type=returns.ReturnType.JSON,
                    )
                else:
                    raise ValueError("Nothing to fetch/post!")

        params = self.params_filter(
            {"hookType": 1, "param": server_url, "txnType": transactions_type or 2}
        )

        async with self._session.put(url, params=params) as response:
            return await self.make_return(
                response, webhook.WebHook, forces_return_type=returns.ReturnType.JSON
            )

    async def delete_hooks(self, hook_id: Optional[str] = None) -> dict:
        """
        Removes hooks by hook_id if exists
        :param hook_id: active hook_id
        :return: json-response
        """
        if not hook_id:
            hook = await self.hooks()
            hook_id = (
                hook["hookId"] if isinstance(hook, dict) else hook.hook_id
            )  # type: ignore

        url = Urls.Hooks.delete.format(hook_id)
        async with self._session.delete(url) as response:
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
            warnings.warn(
                "Seems you didn't have registered webhooks. Setting new to %s"
                % new_url,
                RuntimeWarning,
            )

        return await self.hooks(new_url, transactions_types)

    # end region

    # balance related region
    async def balance(self, alias: Optional[str] = None) -> balance.Balance:
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
            async with self._session.get(url) as response:
                return await self.make_return(response, balance.Balance)

        url = Urls.Balance.set_new_balance.format(self.phone_number, alias)

        async with self._session.patch(url, data={"defaultAccount": True}) as response:
            return await response.json()

    async def available_balances(self) -> List[offer.Offer]:
        """
        Get aliases of available offers
        :return: list[Offer]
        """
        if not self.phone_number:
            self._raise_for_phone()

        url = Urls.Balance.available_aliases

        async with self._session.get(url) as response:
            return await self.make_return(response, offer.Offer)

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

        async with self._session.post(url, data=payment_type.json()) as response:
            return await self.make_return(response, payment.Payment)

    async def commission(
        self,
        amount: float,
        receiver: Union[str, int],
        provider: Union[enums.Provider] = enums.Provider.QIWI_WALLET,
        *,
        currency: Union[currencies.CurrencyModel, str, int] = "643",
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

        currency_isoformat = self._get_currency_isoformat(currency)

        data = self.json_module.serialize(
            {
                "account": phone_module.parse_phone(receiver),
                "paymentMethod": {"type": "Account", "accountId": currency_isoformat},
                "purchaseTotals": {
                    "total": {"amount": amount, "currency": currency_isoformat}
                },
            }
        )

        async with self._session.post(url, data=data) as response:
            return await self.make_return(response, commission.Commission)

    async def detect_provider(
        self, phone: Optional[Union[str, int]] = None
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
        params = self.params_filter({"phone": phone or self.phone_number})

        headers = {
            "Accept": "application/json",
            "Content-type": "application/x-www-form-urlencoded",
        }

        async with self._session.get(url, params=params, headers=headers) as response:
            return await self.make_return(response, phone_provider.Provider)

    # end region

    # blocking op setup -> run server
    def idle(
        self,
        host: str = "localhost",
        port: int = 7494,
        path: Optional[str] = None,
        app: Optional[web.Application] = None,
    ):
        """
        :param host: server host
        :param port: server port that open for tcp/ip trans.
        :param path: path for qiwi that will send requests
        :param app: pass web.Application if you want, common-use - aiogram powered webhook-bots
        """
        app = app or web.Application()
        server.setup(self.handler_manager, app, path)

        web.run_app(app, host=host, port=port)

    def configure_for_app(self, app, path=None):
        """
        If you want to implement your start_webhook execution use this method and get configured listener with
        configured web-view for passed path[see default in webhooks/server.py]
        :param app: aiohttp.web.Application initialized
        :param path: url path
        """
        server.setup(self.handler_manager, app, path)

    # end region
