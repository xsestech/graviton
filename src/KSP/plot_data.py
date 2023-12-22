import matplotlib.pyplot as plt
import numpy as np


from src.KSP.config import get_ksp_settings
from src.KSP.utlis import triangle_integrate, load_data

settings = get_ksp_settings()

# Загрузим объекты
velocities = load_data("velocities.joblib")
cords = load_data("cords.joblib")
times = load_data("time.joblib")
math_v = load_data("math_v.joblib")
math_y = load_data("math_y.joblib")
math_t = load_data("math_t.joblib")
# Найдем момент T0, и вычтем его из всего времени, переведём время в часы
times /= 60
arg_range = np.argwhere((times >= 225800) & (times <= 226000))
times -= times[np.where(velocities == np.max(velocities[arg_range]))]
# Переведем скорость в км/с
velocities /= 1000
# Найдем все индексы, которые входят во временной диапазон
index_in_time_range = np.argwhere(np.abs(times) <= settings.TIME_RANGE * 60)
# Получим график
plt.plot(times[index_in_time_range], velocities[index_in_time_range], 'r')
plt.title("Скорость аппарата в KSP")
plt.ylabel("Скорость, км/с")
plt.xlabel("Время относительно T0, мин")
plt.savefig('../../artifacts/ksp_speed.png', dpi=100)

# Сравнительный график
plt.plot(times[index_in_time_range], velocities[index_in_time_range], 'r', label='KSP')
plt.plot(math_t, math_v, 'b', label='Модель')
plt.title("Сравнение модели и KSP")
plt.ylabel("Скорость, км/с")
plt.xlabel("Время относительно T0, мин")
plt.legend(loc='best')
plt.savefig('../../artifacts/compare_math_ksp_speed.png', dpi=100)
plt.show()

# Оставим только нужное
cords1 = np.squeeze(cords[index_in_time_range])
times1 = np.squeeze(times[index_in_time_range])

# Проверим второй закон кеплера
# KSP
print("Дисперсия в KSP:")
plt.title("KSP")
ares_tri_ksp, time_err_ksp, sample_error_ksp = triangle_integrate(cords1, times1, 10)
plt.title("KSP")
plt.bar(np.arange(settings.N_SPLITS), ares_tri_ksp, color='r')
plt.show()

# Модель
print("Дисперсия в модели:")
plt.title("Модель")
ares_tri_math, time_err_math, sample_error_math = triangle_integrate(math_y.T[:, 0:3], math_t, settings.N_SPLITS)
plt.title("Модель")
plt.bar(np.arange(settings.N_SPLITS), ares_tri_math)
plt.show()
