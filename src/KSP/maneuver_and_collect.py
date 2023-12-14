import os
import time
import krpc
import matplotlib.pyplot as plt
import joblib

DATA_PATH = '../../data/'
if not os.path.exists(DATA_PATH):
    os.mkdir(DATA_PATH)
conn = krpc.connect()

spc = conn.space_center
vessel = conn.space_center.active_vessel
vessel.control.activate_next_stage()

vessel.control.sas = True
time.sleep(1)
for _ in range(100):
    vessel.control.sas_mode = vessel.control.sas_mode.prograde
time.sleep(1)
vessel.control.throttle = 1.0

periapsis_altitude = conn.get_call(getattr, vessel.orbit, 'periapsis_altitude')
expr = conn.krpc.Expression.greater_than(
    conn.krpc.Expression.call(periapsis_altitude),
    conn.krpc.Expression.constant_double(250000))
event = conn.krpc.add_event(expr)
with event.condition:
    event.wait()
vessel.control.throttle = 0
# Начинаем снимать данные
velocities = []
cords = []
times = []
position = conn.add_stream(vessel.position, vessel.orbit.body.reference_frame)
velocity = conn.add_stream(getattr, vessel.flight(
    vessel.orbit.body.reference_frame), 'speed')
ut = conn.add_stream(getattr, conn.space_center, 'ut')

work = True
try:
    time.sleep(2)
    for _ in range(1000):
        spc.rails_warp_factor = 3
    while work:
        cords.append(position())
        velocities.append(velocity())
        times.append(ut())
        time.sleep(0.1)
except KeyboardInterrupt:
    spc.rails_warp_factor = 0
    joblib.dump(cords, os.path.join(DATA_PATH, "cords.joblib"))
    joblib.dump(velocities, os.path.join(DATA_PATH, "velocities.joblib"))
    joblib.dump(times, os.path.join(DATA_PATH, "time.joblib"))
    work = False
    plt.plot(velocities)
    plt.show()
    exit(0)
