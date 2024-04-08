#  coding: utf-8
import numpy as np

RANDOM_POINTS = False
if RANDOM_POINTS:
    for i in range(10):
        POINTS.append((
            np.random.randint(0, 10),
            np.random.randint(0, 10)
        ))
else:
    POINTS = [
        (1, 2),
        (1, 3),
        (2, 1),
        (2, 4),
        (3, 0),
        (3, 5),
        (4, 0),
        (4, 5),
        (5, 1),
        (5, 4),
        (6, 2),
        (6, 3),
    ]

POINT_COUNT = len(POINTS)
