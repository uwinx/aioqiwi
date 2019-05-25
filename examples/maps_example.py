import asyncio

from aioqiwi.terminals import Polygon, QiwiMaps
from aioqiwi.terminals.utils import get_distance


async def qiwi_maps():
    my_lat_lon = (55.719384, 37.781102)
    polygon = Polygon((55.690881, 37.386282), (55.580184, 37.826078))

    async with QiwiMaps() as maps:
        terminals = await maps.terminals(polygon, zoom=12, cache_terminals=True)

        for terminal in terminals:
            print(f'{terminal.terminal_id:<10} is {get_distance(terminal.Coordinate.latlon, my_lat_lon):.2f} m. away')


asyncio.run(qiwi_maps())
