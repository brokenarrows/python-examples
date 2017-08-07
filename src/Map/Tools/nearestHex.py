#!/usr/bin/env

import math


def generate_hex(data):
    """
    Inspiration: https://github.com/d3/d3-hexbin

    From the data points we generate an array of hex bins
    :param data: data array
    """
    hexagons = {}

    for point in data:
        x, y = point[0], point[1]

        point_x_nearest = _nearest_point(x)
        point_y_nearest = _nearest_point(y)

        point_1 = _euclidean_distance(x, y, point_x_nearest[0], point_y_nearest[0])
        point_2 = _euclidean_distance(x, y, point_x_nearest[1], point_y_nearest[1])

        if point_2 > point_1:
            hex = str([point_x_nearest[1], point_y_nearest[1]])
        else:
            hex = str([point_x_nearest[0], point_y_nearest[0]])

        hexagons[hex] = 1 + hexagons.get(hex, 0)

    return hexagons


def _euclidean_distance(x, y, x1, y1):
    """
    Returns the Euclidean distance from
    Very often, especially when measuring the distance in the plane, we use the formula for the Euclidean distance.
    According to the Euclidean distance formula, the distance between two points in the plane with coordinates
    [x,y] to [x1,y1]is given by
    dist((x, y), (a, b)) = √(x - a)² + (y - b)²
    """
    return math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))


def _nearest_point(value):
    """
    Returns the nearest positions bins
    :param value: X or Y value
    :returns: tuple of closest bin center points
    """
    width = 2
    div, mod = (value // width / 2, value % width / 2)
    result = width / 2 * (div + (1 if div % 2 == 1 else 0))
    return [result]
