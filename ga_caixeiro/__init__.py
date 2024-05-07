#  coding: utf-8
import numpy as np

COMPLEX_FIGURES = [
    # Maior fitness até agora: -151 -> [ 4 11  2 23 13 21 12 29 22  3  8 26 18 20 14  7  0  9  1  5 16  6 27 19 28 25 24 17 10 15]
    # Config: NG: 100, NPM: 20, SPP: 150, KE: 20, CT: scattered, MT: random, MPG: 5
    [(16,  9), (28, 0), (20, 5), ( 4,  7), (26, 11), (26,  0), (25, 29), (16, 11), ( 3, 28), (22,  1),
     (22, 20), (26, 7), ( 4, 5), (12,  6), (16, 14), (26, 17), (29, 23), (11, 16), ( 8, 26), (14, 25),
     (12, 23), ( 9, 4), ( 1, 6), (16,  4), (10, 14), ( 4, 10), ( 6, 28), (23, 28), ( 4, 10), ( 1,  1)],

    # Maior fitness até agora: -67 -> [ 2  0 13 16  1 14 15  5 10  8 11  9  7  3 12 19  4 17  6 18]
    [(1, 6), (12, 15), (3, 5), (13, 11), (15, 6), (12, 1), (15, 2), (6, 6), (7, 1), (5, 4), (13, 0), (4, 2), (13, 9),
     (2, 10), (16, 10), (12, 3), (4, 9), (19, 4), (7, 3), (14, 6)]
]

RANDOM_POINTS = True
if RANDOM_POINTS:
    FIGURE = 0
    if FIGURE >= 0:
        POINTS = COMPLEX_FIGURES[FIGURE]
    else:
        amount_of_points = 20
        POINTS = []
        for i in range(amount_of_points):
            POINTS.append((
                np.random.randint(0, amount_of_points),
                np.random.randint(0, amount_of_points)
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
print(POINTS)
POINT_COUNT = len(POINTS)
