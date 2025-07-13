import numpy as np
import matplotlib.pyplot as plt

# 설정값
initial_speed_kms = 7.35 

# 상수
G = 6.67430e-11
M = 5.972e24
R = 6.371e6  # 지구 반지름 [m]
LEO_ALT = 1000e3  # 고도 1000km
dt = 1
max_time = 50000

# 초기 위치/속도 
x = R + LEO_ALT
y = 0
vx = 0
vy = initial_speed_kms * 1000  # km/s → m/s

positions_x = []
positions_y = []

crashed = False
escaped = False

for _ in range(max_time):
    r = np.sqrt(x**2 + y**2)
    if r < R:
        crashed = True
        break
    if r > 15 * R:
        escaped = True
        break

    a = G * M / r**2
    ax = -a * x / r
    ay = -a * y / r

    vx += ax * dt
    vy += ay * dt
    x += vx * dt
    y += vy * dt

    positions_x.append(x)
    positions_y.append(y)

# 시각화

positions_x_km = np.array(positions_x) / 1000
positions_y_km = np.array(positions_y) / 1000
R_km = R / 1000

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_facecolor('black')

# 지구 그리기
earth = plt.Circle((0, 0), R_km, color='blue', zorder=0)
ax.add_patch(earth)

# 궤도 궤적
ax.plot(positions_x_km, positions_y_km, color='red', linewidth=2)

# 그래프 범위 자동 조정
buffer = R_km * 0.5
x_min, x_max = positions_x_km.min() - buffer, positions_x_km.max() + buffer
y_min, y_max = positions_y_km.min() - buffer, positions_y_km.max() + buffer
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)

if crashed:
    status = "지구에 충돌"
elif escaped:
    status = "지구 탈출"
else:
    status = "안정된 궤도"

plt.title(f"(1000km) 시작 / 속도: {initial_speed_kms} km/s → {status}", color='white')
plt.xlabel("X 위치 (km)")
plt.ylabel("Y 위치 (km)")
plt.show()
