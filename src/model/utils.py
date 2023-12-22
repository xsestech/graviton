import numpy as np

from src.model.config import get_model_settings

settings = get_model_settings()


def make_plot(y, position, elev, azim, roll, fig):
    """
    Ввыод подграфика скорости с настройками камеры


    :param y: Координата
    :param position: позиция подграфика
    :param elev: высота камеры
    :param azim: азимут камеры
    :param roll: крен камеры
    :param fig: matplotlib figure
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
