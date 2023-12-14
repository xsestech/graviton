import os

import joblib
import matplotlib.pyplot as plt
import numpy as np

DATA_PATH = '../../data'
TIME_RANGE = 1  # В часах

# Загрузим объекты
velocities = np.array(joblib.load(os.path.join(DATA_PATH, "velocities.joblib")))
times = np.array(joblib.load(os.path.join(DATA_PATH, "time.joblib")))
math_v = joblib.load(os.path.join(DATA_PATH, "math_v.joblib"))
math_t = joblib.load(os.path.join(DATA_PATH, "math_t.joblib"))
# Найдем момент T0, и вычтем его из всего времени, переведём время в часы
times -= times[np.argmax(velocities)]
times /= 60
# Переведем скорость в км/с
velocities /= 1000
# Найдем все индексы, которые входят во временной диапазон
index_in_time_range = np.argwhere(np.abs(times) <= TIME_RANGE * 60)
# Получим график
plt.plot(times[index_in_time_range], velocities[index_in_time_range], 'r')
plt.title("Скорость аппарата в KSP")
plt.ylabel("Скорость, км/с")
plt.xlabel("Время относительно T0, мин")
plt.savefig('../../artifacts/ksp_speed.png', dpi=100)
# Сравнительный график
plt.plot(times[index_in_time_range], velocities[index_in_time_range], 'r', label='KSP')
plt.plot(math_t, math_v, 'g', label='Модель')
plt.title("Сравнение модели и KSP")
plt.ylabel("Скорость, км/с")
plt.xlabel("Время относительно T0, мин")
plt.legend(loc='best')
plt.savefig('../../artifacts/compare_math_ksp_speed.png', dpi=100)
