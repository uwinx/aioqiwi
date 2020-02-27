# install geopy

import asyncio

from aioqiwi.terminals import Polygon, QiwiMaps
from geopy.distance import distance


async def qiwi_maps():
    my_lat_lon = (55.719384, 37.781102)
    polygon = Polygon((55.690881, 37.386282), (55.580184, 37.826078))

    maps = QiwiMaps()
    terminals = await maps.terminals(polygon, zoom=12, cache_terminals=True)

    for terminal in terminals:
        terminal_latlon = (terminal.coordinate.latitude, terminal.coordinate.longitude)
        print(
            f"{terminal.terminal_id:<10} is {distance(terminal_latlon, my_lat_lon).km:.2f} m. away"
        )

    await maps.close()


asyncio.run(qiwi_maps())
