import math


ER = 6371  # ~EARTH-RADIUS


def get_distance(apack: tuple, bpack: tuple):
    """
    Get distance between two geo-points
    :param apack: tuple of lat-lon of point A
    :param bpack: tuple of lat-lon of point B
    :return:
    """
    lata, lona = apack
    latb, lonb = bpack

    delta_lat = math.radians(latb - lata)
    delta_lon = math.radians(lonb - lona)

    a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + math.cos(
        math.radians(lata)
    ) * math.cos(math.radians(latb)) * math.sin(delta_lon / 2) * math.sin(delta_lon / 2)

    return ER * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
