import os
import time

import joblib
import krpc
import matplotlib.pyplot as plt

from src.KSP.config import get_ksp_settings

# Конфиг
settings = get_ksp_settings()

# Создаем папку для сохранения данных
if not os.path.exists(settings.DATA_PATH):
    os.mkdir(settings.DATA_PATH)

# Подключаемся к серверу krpc
conn = krpc.connect()
spc = conn.space_center
vessel = conn.space_center.active_vessel

# Доводим орбиту до нужной
if settings.IS_CHEAT_ON:
    # Отделяем лишнюю ступень и включаем САС
    vessel.control.activate_next_stage()
    vessel.control.sas = True
    time.sleep(settings.WAIT_TIME)

    # Меняем вектор направления ракеты на "по движению"
    for _ in range(settings.N_REQUESTS):
        vessel.control.sas_mode = vessel.control.sas_mode.prograde
    time.sleep(settings.WAIT_TIME)
    vessel.control.throttle = 1.0

    # Держим двигатели включенными, пока не достигнем нужной высоты в перигее
    periapsis_altitude = conn.get_call(getattr, vessel.orbit, 'periapsis_altitude')
    expr = conn.krpc.Expression.greater_than(
        conn.krpc.Expression.call(periapsis_altitude),
        conn.krpc.Expression.constant_double(settings.TARGET_PERIAPSIS))
    event = conn.krpc.add_event(expr)
    with event.condition:
        event.wait()
    # Выключаем двигатели
    vessel.control.throttle = 0

# Начинаем снимать данные
velocities = []
cords = []
times = []
venus_frame = spc.bodies['Eve'].reference_frame  # Берем Венеру, как точку отсчета
# Для более эффективного снятия данных воспользуется потоками(stream)
position = conn.add_stream(vessel.position, venus_frame)
velocity = conn.add_stream(getattr, vessel.flight(
    venus_frame), 'velocity')
ut = conn.add_stream(getattr, conn.space_center, 'ut')

work = True
try:
    # Данный блок немного костыльный, но по-другому гарантировано установить ускорение времени не получилось
    time.sleep(settings.WAIT_TIME)
    for _ in range(settings.N_REQUESTS):
        spc.rails_warp_factor = settings.WARP_FACTOR
    # Запускаем цикл снятия данных
    while work:
        cords.append(position())
        velocities.append(velocity())
        times.append(ut())
        time.sleep(settings.DATA_DELAY)
except KeyboardInterrupt:  # Остановка по ctl-c
    spc.rails_warp_factor = 0  # Выключим ускорение времени
    # Сохраним массивы с помощью joblib
    joblib.dump(cords, os.path.join(settings.DATA_PATH, "cords_2.joblib"))
    joblib.dump(velocities, os.path.join(settings.DATA_PATH, "velocities_2.joblib"))
    joblib.dump(times, os.path.join(settings.DATA_PATH, "time_2.joblib"))

    # Выведем график
    plt.plot(velocities)
    plt.show()

    # Выйдем из программы
    work = False
    exit(0)
