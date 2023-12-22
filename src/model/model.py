import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from config import ModelSettings
from src.model.utils import make_plot

settings = ModelSettings()
fig = plt.figure(dpi=100)


def dr_dt(t, y):
    """
    Решение дифференциального уравнения второго прядка для нахождения скорости и координаты аппарата.
    :param y: y[:3] - позиция, y[3:] - скорость
    :param t: время
    :return:
    """
    mu = settings.G * settings.VENUS_MASS
    r = np.linalg.norm(y[:3])
    dr = y[3:]
    dv = - (mu / (r ** 3)) * y[:3]
    dy = np.concatenate([dr, dv])
    return dy


# Создадим папку для хранения артефактов
if not os.path.exists('../../artifacts'):
    os.mkdir('../../artifacts')

# Задаем начальную позицию
v0 = np.array([0, settings.V0, 0], dtype=np.float64)
r0 = np.array([settings.H0 + settings.VENUS_R, 0, 0], dtype=np.float64)
y0 = np.concatenate([r0, v0])

# Считаем до начального момента
print("Cчитаем до T0...", end="")
t_minus_eval = np.arange(0, -settings.TIME_RANGE, -settings.TIME_STEP)
y_minus = solve_ivp(dr_dt, [0, -settings.TIME_RANGE], y0, t_eval=t_minus_eval, method=settings.METHOD,
                    vectorized=True).y
print("Готово")

# Считаем после начального момента
print("Cчитаем после T0...", end="")
t_plus_eval = np.arange(0, settings.TIME_RANGE, settings.TIME_STEP)
y_plus = solve_ivp(dr_dt, [0, settings.TIME_RANGE], y0, t_eval=t_plus_eval, method=settings.METHOD, vectorized=True).y
print("Готово")

# Объединим данные
print("Объединяем данные...", end="")
y = np.concatenate([np.flip(y_minus, axis=1), y_plus[:, 1:]], axis=1)
print("Готово")

# Выведем графики
print("Делаем график координаты...", end="")

make_plot(y, 121, None, None, None, fig)
make_plot(y, 122, 90, -90, 0, fig)

plt.savefig(f'../../artifacts/coordinates_graph.png')
plt.show()
print("Готово")

print("Делаем график скорости...", end="")
# Считаем модуль скорости
v = np.linalg.norm(y[3:], axis=0) / 1000
t = np.concatenate([np.flip(t_minus_eval, axis=0), t_plus_eval[1:]]) / 60

# Выводим график
plt.plot(t, v)
plt.title("Скорость аппарата")
plt.ylabel("Скорость, км/с")
plt.xlabel("Время относительно T0, мин")

plt.savefig('../../artifacts/speed_graph.png', bbox_inches='tight')
plt.show()

joblib.dump(v, '../data/math_v.joblib')
joblib.dump(t, '../data/math_t.joblib')
joblib.dump(y, '../data/math_y.joblib')

print("Готово")
