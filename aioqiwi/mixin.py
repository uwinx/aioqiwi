import json
import importlib

from aiohttp import client

from .models import utils

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
    def param_filter(dictionary: dict):
        return {k: v for k, v in dictionary.items() if v is not None}

    async def _make_return(self, resp, *models, spec_ignore=False):
        data = await resp.json()
        if spec_ignore:
            return utils.ignore_specs_get_list_of_models(data, *models)
        return utils.json_to_model(data, *models) if self.as_model else resp

    @staticmethod
    def _new_http_session(api_hash: str, timeout: float or int = None):
        headers = {
            "Accept": "application/json",
            "Content-type": "application/json",
            "Authorization": f"Bearer {api_hash}",
        }

        timeout = client.ClientTimeout(total=timeout or 60)

        return client.ClientSession(
            headers=headers or {}, timeout=timeout, json_serialize=serialize
        )

