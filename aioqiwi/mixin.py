import json
import importlib

from aiohttp import client

from .models import utils
from .utils.currency_utils import Currency

# helpers
TZD = "03:00"

serialize = json.dumps
deserialize = json.loads

# get json (d1)e(n2)coder
for json_lib in ["rapidjson", "ujson", "json"]:
    try:
        serialize = importlib.import_module(json_lib).dumps
        deserialize = importlib.import_module(json_lib).loads
        break
    except ImportError:
        continue


class QiwiMixin:
    TZD = TZD
    as_model = True

    @staticmethod
    def _param_filter(dictionary: dict):
        """
        pop NoneType values and convert everything to str, designed?for=params
        :param dictionary: source dict
        :return: filtered dict
        """
        return {k: str(v) for k, v in dictionary.items() if v is not None}

    async def _make_return(self, resp, *models, spec_ignore=False):
        """
        Convenient way to do return FOR ME
        :param resp: server-response
        :param models: api-model
        :param spec_ignore: ignore keys in response get list-like value and return list of model:`value`
        :return: models in model | list of models
        """
        data = await resp.json()
        print(data)
        if spec_ignore:
            return utils.ignore_specs_get_list_of_models(data, *models)
        return utils.json_to_model(data, *models) if self.as_model else resp

    @staticmethod
    def _new_http_session(api_hash: str, timeout: float or int = None, *, ctype: str = None, atype: str = None):
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
            "Authorization": f"Bearer {api_hash}" if api_hash else None,
        }

        timeout = client.ClientTimeout(total=timeout or 60)

        return client.ClientSession(
            headers=QiwiMixin._param_filter(headers), timeout=timeout, json_serialize=serialize
        )

    @staticmethod
    def get_currency(currency: str or int or Currency):
        """
        Get currency lazy method
        :param currency: currency like ISO-4217, 3-len curr-codes
        :return: currency-code
        """
        return (
            currency.code
            if isinstance(currency, Currency.currency)
            else Currency[currency].code
        )


