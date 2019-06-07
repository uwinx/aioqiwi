import json
import importlib
import logging

from .models import utils, exceptions
from .exceptions import ApiBaseException

# DEFAULT MOSCOW-TIMEZONE
MOSCOW_TZD = "03:00"
DATETIME_FMT = '%Y-%m-%dT%H:%M:%S+{}'

logger = logging.getLogger('aioqiwi')

serialize = json.dumps
deserialize = json.loads
json_module = 'json'

# get json (d1)e(n2)coder
for json_lib in ["rapidjson", "ujson"]:
    try:
        serialize = importlib.import_module(json_lib).dumps
        deserialize = importlib.import_module(json_lib).loads
        json_module = json_lib
        break
    except ImportError:
        continue


class Requests:
    TZD = MOSCOW_TZD

    @property
    def _date_fmt(self):
        return DATETIME_FMT.format(self.TZD)

    as_model = True

    async def _make_return(self, resp, *models, spec_ignore=False, force_non_model=False):
        """
        todo: BETTER-ERROR HANDLING
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
            logger.error(exc)
            return data, resp

        ret_func = (
            utils.ignore_specs_get_list_of_models
            if spec_ignore
            else utils.json_to_model
        )

        try:
            if not force_non_model:
                return ret_func(data, *models) if self.as_model else data
            return data
        except exceptions.ModelConversionError as error:
            raise ApiBaseException(error.json)

    def parse_date(self, date):
        return date if isinstance(date, str) else date.strftime(self._date_fmt)

    @property
    def listeners(self):
        if hasattr(self, '_handler'):
            return self._handler.registered_handlers
