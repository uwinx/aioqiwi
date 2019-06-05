from aiohttp import client

from ..utils.currencies.currency_utils import Currency
from ..requests import serialize


def params_filter(dictionary: dict):
    """
    Pop NoneType values and convert everything to str, designed?for=params
    :param dictionary: source dict
    :return: filtered dict
    """
    return {k: str(v) for k, v in dictionary.items() if v is not None}


def get_currency(currency):
    """
    Get currency lazy method
    :param currency: currency like ISO-4217, 3-len curr-codes
    :return: currency-code
    """
    if isinstance(currency, Currency.currency):
        return currency

    return Currency[currency]


def new_http_session(
    api_hash: str, timeout: float or int = None, *, ctype: str = None, atype: str = None
):
    """
    Create new instance of ClientSession
    :param api_hash: private key
    :param timeout: client timeout
    :param ctype: content-type
    :param atype: accept-type
    :return: aiohttp.client.ClientSession
    """
    headers = {
        "Accept": atype or "application/json",
        "Content-type": ctype or "application/json",
        "Authorization": f"Bearer {api_hash}" if api_hash else None,  # eg:maps
    }

    timeout = client.ClientTimeout(total=timeout or 60)

    return client.ClientSession(
        headers=params_filter(headers), timeout=timeout, json_serialize=serialize
    )
