from typing import Tuple

from ..utils import currencies as cur
from ..models import history, updates


class BeautifulSum:
    def __init__(
        self, payment_sum: history.History.Sum or updates.QiwiUpdate.Payment.Sum
    ):
        """
        :param payment_sum: object `sum` from history or qiwi-update objects

        .. code-block:: python3
        >>> async def foo():
        ...     async with QiwiAccount('my_hash', '') as client:
        ...         return BeautifulSum((await client.history(20)).data[-1]).humanize
        ...
        >>> asyncio.run(foo())
        """
        self.amount, self.currency = payment_sum.amount, payment_sum.currency

    @property
    def human_currency(self) -> cur.Currency:
        """
        Get beautiful payment.sum.currency info, returns russian rubles by default
        :return: Gets currency by ISO-4217 code sent by qiwi, russian rubles by default
        """
        return Currency[self.currency]

    @property
    def human_amount(self):
        """
        Get beautiful formatted payment.sum.amount
        :return:
        """
        return f"{self.amount:,}"

    @property
    def humanize(self):
        return f"{self.human_amount} {self.human_currency.name}"

    @property
    def pretty(self):
        return f"{self.human_amount:<12} {self.human_currency.symbol_native}"

    def __repr__(self):
        return self.pretty


class Currency:
    """
    Easy to use class to get info abot currency
    >>> usd = Currency['840']
    >>> usd
    ... Currency(code='USD', decimal_digits=2, name='US Dollar', name_plural='US dollars', rounding=0, symbol='$', symbol_native='$')
    >>> usd.symbol
    ... '$'
    """

    @staticmethod
    def __class_getitem__(currency_code) -> cur.Currency:
        """
        Implements class-based getitem behaviour
        >>> Currency.__class_getitem__('840').symbol
        ... '$'
        >>> Currency['840'].symbol
        ... '$'
        >>> Currency['USD'].symbol
        ... '$'
        :param currency_code: ISO 4217 string or CODE
        :return: Currency object
        """
        try:
            if currency_code.isdigit():
                return cur.described.get(cur.codes_number[str(currency_code)])
            else:
                return cur.described.get(currency_code.upper())
        except KeyError:
            raise ValueError(
                f"Currency code `{currency_code}` was not found in database"
            )

    @staticmethod
    def get_raw(
        amount: float or int, currency_code: str or int, currency_attr: str = None
    ) -> Tuple[str, cur.Currency]:
        """
        Get pair of 3dig formatted amount
        >>> Currency.get_raw(20984, 840, 'symbol')
        ... ('20,984', '$')
        >>> Currency.get_raw(253543, 'usd', 'symbol')
        ... ('253,543', '$')
        :param amount: any number of amount
        :param currency_code:
        :param currency_attr:
        :return:
        """
        currency = Currency[currency_code]

        if currency_attr and hasattr(currency, currency_attr):
            currency = getattr(currency, currency_attr)

        return f"{amount:,}", currency

    currency = cur.Currency
