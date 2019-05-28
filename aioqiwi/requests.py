import json
import importlib
import logging

from .models import utils

# DEFAULT MOSCOW-TIMEZONE
MOSCOW_TZD = "03:00"
logger = logging.getLogger('aioqiwi')

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


class Requests:
    TZD = MOSCOW_TZD
    as_model = True

    async def _make_return(self, resp, *models, spec_ignore=False):
        """
        todo: ERROR HANDLING
        Convenient way to do return
        :param resp: server-response
        :param models: api-model
        :param spec_ignore: ignore keys in response get list-like value and return list of model:`value`
        :return: models in model | list of models | model
        """
        data = await resp.read()

        try:
            data = deserialize(data)
        except TypeError as exc:
            logger.error("%s exc." % exc.with_traceback())
            return data, resp

        ret_func = (
            utils.ignore_specs_get_list_of_models
            if spec_ignore
            else utils.json_to_model
        )
        return ret_func(data, *models) if self.as_model else data

    def parse_date(self, date):
        return date if isinstance(date, str) else date.strftime(self.TZD)
