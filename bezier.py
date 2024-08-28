from random import sample

import numpy as np
import numpy.typing as npt
import math


def generate_ctrlpoints(degree: int) -> npt.ArrayLike:
    """Minimum 2 points required"""
    ctrl_points = np.random.randint((0, 0), (400, 400), (degree, 2))
    return ctrl_points


def bernstein(t, n: int, i: int) -> int:
    """
    Generates a Bernstein basis polynomial
    reference: https://en.wikipedia.org/wiki/Bernstein_polynomial

    :param t:
    :param n:
    :param i:
    :return:
    """
    return math.comb(n, i) * math.pow(t, i) * math.pow((1 - t), (n - i))


def generate_bezier(points, t) -> tuple[float, float]:
    """
    Generate Bezier curve coordinates
    reference: [explicit terminology] https://en.wikipedia.org/wiki/B%C3%A9zier_curve

    :param points:
    :param t:
    :return:
    """
    degree = len(points) - 1
    x = y = 0
    for i, pos in enumerate(points):
        bern_coeff = bernstein(t, degree, i)
        x += pos[0] * bern_coeff
        y += pos[1] * bern_coeff
    return (x, y)

def bezier_curve_points(degree, smoothness):
    """
    Produce the coordinates of the curve to draw

    :param degree:
    :param smoothness:
    :return:
    """
    bezier_coords = []
    ctrl_points = generate_ctrlpoints(degree)
    sample_points = np.linspace(0, 1, smoothness)

    for i, t in enumerate(sample_points):
        bezier_coords.append(generate_bezier(ctrl_points, t))

    return bezier_coords, ctrl_points