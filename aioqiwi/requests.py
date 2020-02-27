import json
import logging
import importlib

from pydantic import ValidationError

from .exceptions import ApiBaseException

# DEFAULT MOSCOW-TIMEZONE
MOSCOW_TZD = "03:00"
DATETIME_FMT = "%Y-%m-%dT%H:%M:%S+{}"

logger = logging.getLogger("aioqiwi")

serialize = json.dumps
deserialize = json.loads
json_module = "json"

for json_lib in ["orjson", "ujson", "rapidjson"]:
    try:
        serialize = importlib.import_module(json_lib).dumps  # type: ignore
        deserialize = importlib.import_module(json_lib).loads  # type: ignore
        json_module = json_lib
        break
    except ImportError:
        continue


class Requests:
    TZD = MOSCOW_TZD  # default qiwi timezone (moscow)

    @property
    def _date_fmt(self):
        return DATETIME_FMT.format(self.TZD)

    as_model = True

    async def _make_return(
        self, resp, model, force_non_model=False, as_list: bool = False
    ):
        """
        Convenient way to do return
        :param resp: server-response
        :param model: api-model
        """
        data = await resp.read()

        if not data:
            raise ApiBaseException("Invalid data obtained")

        try:
            data = deserialize(data)
        except TypeError as exc:
            logger.error(exc)
            raise ApiBaseException("JSON parsing error")

        try:
            if not force_non_model:
                if not as_list:
                    return model(**data) if self.as_model else data
                else:
                    return [model(**t) for t in data] if self.as_model else data
            return data
        except ValidationError as error:
            raise ApiBaseException(error.json())

    def parse_date(self, date):
        return date if isinstance(date, str) else date.strftime(self._date_fmt)
