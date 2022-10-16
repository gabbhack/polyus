# размер отрисовка
import math
from typing import Optional

import cv2
import numpy as np

height_mm = 1600
height = 720
trapez_1 = (
    923,
    235,
    (1 / math.tan(55.8 * math.pi / 180) + 1 / math.tan(59.1 * math.pi / 180)),
)
trapez_2 = (
    623,
    53,
    (1 / math.tan(46.9 * math.pi / 180) + 1 / math.tan(59.1 * math.pi / 180)),
)
trapez_3 = (
    542,
    86,
    (1 / math.tan(46.9 * math.pi / 180) + 1 / math.tan(49.3 * math.pi / 180)),
)
colors = [
    [0, 0, 153],
    [255, 0, 5],
    [255, 0, 219],
    [255, 209, 0],
    [56, 255, 0],
    [0, 255, 250],
    [178, 178, 225],
    [255, 255, 255],
]

# ф-ия для расстояния
flag_detected = False
flag_zero_detect = False
count = 0


def distance(array):
    global count, flag_detected, flag_zero_detect
    count += 1

    if not flag_detected and array[0] == 1:
        flag_detected = True  # Нашили негабарит
        return None

    elif flag_detected and flag_zero_detect and array[0] == 1:
        flag_detected = True
        flag_zero_detect = False
        s = count
        count = 0
        if s > 30:
            return None
        return s
    elif flag_detected and array[0] == 0:
        flag_zero_detect = True
        return None

    elif array[0] > 1:
        count = 0
        return count
    else:
        return None


def square(
    img: np.array, c1c2_mass: list[list[tuple[int, int]]], big: int = 100
) -> (list[int], float, int, Optional[int]):
    size_sum = 0
    size_mass = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in c1c2_mass:
        c1 = i[0]
        c2 = i[1]
        # считаем размер
        centr = ((c1[0] + (c2[0] - c1[0]) / 2), (c1[1] + (c2[1] - c1[1]) / 2))
        if height - centr[1] <= trapez_1[1]:
            h = height - centr[1]
            b = trapez_1[0] - h * trapez_1[2]
        elif height - centr[1] <= trapez_1[1] + trapez_2[1]:
            h = height - centr[1] - trapez_1[1]
            b = trapez_2[0] - h * trapez_2[2]
        else:
            h = height - centr[1] - trapez_1[1] - trapez_2[1]
            b = trapez_3[0] - h * trapez_3[2]
        coef = height_mm / b
        size = max((c2[0] - c1[0]), (c2[1] - c1[1])) * coef
        size_sum += size
        # определяем класс
        if size > big:
            class_size = 0
        elif 150 < size <= 250:
            class_size = 2
        elif size > 250:
            class_size = 1
        elif 0 < size <= 40:
            class_size = 7
        elif 100 < size <= 150:
            class_size = 3
        elif 40 < size <= 70:
            class_size = 6
        elif 80 < size <= 100:
            class_size = 4
        else:
            class_size = 5
        size_mass[class_size] += 1
        # рисуем
        cv2.rectangle(img, c1, c2, colors[class_size], thickness=2)

    mean_size = size_sum / len(c1c2_mass)
    return size_mass, mean_size, len(c1c2_mass), distance(size_mass)
