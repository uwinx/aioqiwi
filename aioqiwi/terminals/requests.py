import typing

from ..core import requests, returns
from .types.partner import Partner
from .types.polygon import Polygon
from .types.terminal import Terminal
from .urls import urls


class QiwiMaps(requests.Requests):
    def __init__(self, timeout: typing.Optional[float] = None):
        super().__init__(None, acpt_type="application/json;charser=UTF-8", timeout=timeout)

    async def terminals(
        self,
        polygon: Polygon,
        zoom: int = None,
        pop_if_inactive_x_mins: int = 30,
        include_partners: bool = None,
        partners_ids: list = None,
        cache_terminals: bool = None,
        card_terminals: bool = None,
        identification_types: int = None,
        terminal_groups: list = None,
    ) -> typing.List["Terminal"]:  # type: ignore
        """
        Get map of terminals sent for passed polygon with additional params
        :param polygon: aioqiwi.models.polygon.Polygon model or dict with NW SE <l->l>s dict
        :param zoom: https://tech.yandex.ru/maps/doc/staticapi/1.x/dg/concepts/map_scale-docpage/
        :param pop_if_inactive_x_mins: do not show if terminal was inactive for X minutes default 0.5 hours
        :param include_partners: result will include/exclude partner terminals
        :param partners_ids: Not fixed IDS array look at docs
        :param cache_terminals: result will include/exclude cache-acceptable terminals
        :param card_terminals: result will include/exclude card-acceptable terminals
        :param identification_types: `0` - not identified, `1` - partly identified, `2` - fully identified
        :param terminal_groups: look at QiwiMaps.partners
        :return: list of Terminal instances
        """
        url = urls.base

        params = self._filter_dict(
            {
                **polygon.dict,
                "zoom": zoom,
                "activeWithinMinutes": pop_if_inactive_x_mins,
                "withRefillWallet": include_partners,
                "ttpIds": partners_ids,
                "cacheAllowed": cache_terminals,
                "cardAllowed": card_terminals,
                "identificationTypes": identification_types,
                "ttpGroups": terminal_groups,
            }
        )

        response = self.connector.request("GET", url, params=params)
        return await self._make_return(
            response,
            Terminal,
            forces_return_type=returns.ReturnType.LIST_OF_MODELS,  # type: ignore
        )

    async def partners(self) -> typing.List[Partner]:
        """
        Get terminal partners for ttpGroups
        :return: list of TTPGroups
        """

        url = urls.ttp_groups

        response = await self.connector.request(
            "GET",
            url,
            headers={"Content-type": "text/json"}
        )
        return await self._make_return(
            response,
            Partner,
            forces_return_type=returns.ReturnType.LIST_OF_MODELS,  # type: ignore
        )
