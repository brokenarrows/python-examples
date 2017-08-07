# !/usr/bin/env
import sys

import math


def calculate_distance(longitude1, latitude1, longitude2, latitude2, unit):
    """
    A line through three-dimensional space between points of interest on a spherical Earth is the chord of the great
    circle between the points. The central angle between the two points can be determined from the chord length.
    The great circle distance is proportional to the central angle.
    http://www.movable-type.co.uk/scripts/latlong.html
    """

    # convert decimal degrees to radians
    longitude1, latitude1, longitude2, latitude2 = map(math.radians, [longitude1, latitude1, longitude2, latitude2])

    lon = longitude2 - longitude1
    lat = latitude2 - latitude1

    # calculate the bearings
    calculate = math.sin(lat / 2) ** 2 + math.cos(latitude1) * math.cos(latitude2) * math.sin(lon / 2) ** 2
    result = 2 * math.asin(math.sqrt(calculate))

    # default result is in KM
    final = 6367 * result

    # units in meters
    if unit == 'm':
        final *= 1000
    # units in miles
    elif unit == 'miles':
        final *= 0.621371

    return final


def main():
    print('Calculating distance between lat and lon ')
    longitude1 = 0
    latitude1 = 0
    longitude2 = 0
    latitude2 = 0
    unit = 'km'
    print(calculate_distance(longitude1, latitude1, longitude2, latitude2, unit))


if __name__ == '__main__':
    main()
