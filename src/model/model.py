import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp

from config import Settings

settings = Settings()
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


def make_plot(y, position, elev, azim, roll):
    """
    Ввыод подграфика скорости с настройками камеры

    :param y: Координата
    :param position: позиция подграфика
    :param elev: высота камеры
    :param azim: азимут камеры
    :param roll: крен камеры
    :return:
    """
    ax = fig.add_subplot(position, projection='3d')

    ax.view_init(elev=elev, azim=azim, roll=roll)

    # Настройка масштаба
    axis_max = settings.VENUS_R / 1000 * 1.3
    ax.axes.set_xlim3d(left=-axis_max, right=axis_max)
    ax.axes.set_ylim3d(bottom=-axis_max, top=axis_max)
    ax.axes.set_zlim3d(bottom=-axis_max, top=axis_max)

    # График сферы
    u = np.linspace(0, 2 * np.pi, 100)
    v = np.linspace(0, np.pi, 100)
    planet_x = settings.VENUS_R * np.outer(np.cos(u), np.sin(v))
    planet_y = settings.VENUS_R * np.outer(np.sin(u), np.sin(v))
    planet_z = settings.VENUS_R * np.outer(np.ones(np.size(u)), np.cos(v))

    ax.plot(y[0] / 1000, y[1] / 1000, y[2] / 1000, label='Орбита', zorder=10)
    ax.plot_surface(planet_x / 1000, planet_y / 1000, planet_z / 1000, zorder=1)

    ax.set_aspect('equal')


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

make_plot(y, 121, None, None, None)
make_plot(y, 122, 90, -90, 0)

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
print("Готово")
