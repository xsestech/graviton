import os
from typing import Iterable, List, Union

import joblib
import numpy as np
import matplotlib.pyplot as plt

from src.KSP.config import get_ksp_settings

settings = get_ksp_settings()


def load_data(filename: str) -> np.ndarray:
    """
    Загрузка массива из папки по пути DATA_PATH
    :param filename: Имя файла
    :return: массив
    """
    data = joblib.load(os.path.join(settings.DATA_PATH, filename))
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    return data


def calc_std_percent(a: List[float]) -> float:
    """Расчет дисперсии в процентах от среднего"""
    a = np.array(a)
    return np.std(a) / np.mean(a) * 100


def find_closest_index(array: np.array, target: float) -> int:
    """
    Найти индекс ближайшего число, к заданному в массиве numpy
    :param array: массив numpy
    :param target: число, которое ищем
    :return: индекс ближайшего числа
    """
    absolute_diff = np.abs(array - target)
    closest_index = np.argmin(absolute_diff)
    return closest_index


def triangle_integrate(r: np.array, t: np.array, n_splits: int) -> Iterable[Union[List[int], str]]:
    """
    Проверка второго закона Кеплера на модели. Считает площадь на равных по времени промежутках, используя векторное произведение. Выводит дисперсию в процентах и строит графики выбранных промежутков
    :param r: Массив numpy координат
    :param t: Массив numpy времени измерений
    :param n_splits: Количество промежутков
    :return: Массив float c площадями за равные промежутки времени, итоговая абсолютная погрешность во времени и абсолютная погрешность по времени по каждому семплу
    """
    total_time = t[-1] - t[0]
    t = t + abs(np.min(t))
    one_sample_integration_period = (total_time) / n_splits
    n_integrated = 0
    sample_start = 0
    areas = []
    sample_error = []
    integrated_time = 0
    while n_integrated < n_splits:
        # Обрежем один семпл
        sample_end = sample_start + find_closest_index(t[sample_start:], one_sample_integration_period)
        sample_time = t[sample_start:sample_end + 1]
        sample_cords = r[sample_start:sample_end + 1]
        t -= t[sample_end]  # Сдвинем 0 в начало семпла

        # Посчитаем площадь с помощью np.cross
        area = 0.5 * np.sum(np.linalg.norm(np.cross(sample_cords[:-1], sample_cords[1:]), axis=1))
        areas.append(area)

        n_integrated += 1
        current_t_sum = sample_time[-1] - sample_time[0]
        integrated_time += current_t_sum
        sample_start = sample_end
        sample_error.append(one_sample_integration_period - current_t_sum)
        plt.plot(sample_cords[:, 0], sample_cords[:, 1])
    print(f"{calc_std_percent(areas)}%")
    plt.show()
    return areas, total_time - integrated_time, sample_error
