import json
import importlib

from aiohttp import client

from .models import utils
from .utils.currency_utils import Currency

# helpers
TZD = "03:00"

serialize = json.dumps
deserialize = json.loads

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
        return {k: str(v) for k, v in dictionary.items() if v is not None}

    async def _make_return(self, resp, *models, spec_ignore=False):
        data = await resp.json()
        if spec_ignore:
            return utils.ignore_specs_get_list_of_models(data, *models)
        return utils.json_to_model(data, *models) if self.as_model else resp

    @staticmethod
    def _new_http_session(api_hash: str, timeout: float or int = None, *, ctype: str = None, atype: str = None):
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
        return (
            currency.code
            if isinstance(currency, Currency.currency)
            else Currency[currency].code
        )


