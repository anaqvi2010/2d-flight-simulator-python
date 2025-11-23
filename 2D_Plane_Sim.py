import matplotlib
matplotlib.use('macosx')
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ----------------------------
# Initial conditions
# ----------------------------
vx, vy = 30, 5        # initial velocity
x, y = 0, 5           # initial position
rho = 1.225
A = 1.0               # wing area
alpha_deg = 3         # starting AoA
T = 200               # thrust
m = 10
g = 9.81
dt = 0.02
stall_angle_deg = 15   # stall threshold

# ----------------------------
# Plot setup
# ----------------------------
plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(0, 2000)
ax.set_ylim(0, 1200)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.grid(True)

# Trail
trail_x = []
trail_y = []
(trail_line,) = ax.plot([], [], "r-", linewidth=2, alpha=0.6)

# Big airplane triangle
plane_shape = patches.Polygon(
    [[-5, -2], [-5, 2], [10, 0]],  # tail-bottom, tail-top, nose
    closed=True,
    color="blue"
)
ax.add_patch(plane_shape)

# ----------------------------
# Keyboard controls
# ----------------------------
def on_key(event):
    global alpha_deg, T
    if event.key == "up":
        alpha_deg += 1
    elif event.key == "down":
        alpha_deg -= 1
    elif event.key == "right":
        T += 20
    elif event.key == "left":
        T -= 20

fig.canvas.mpl_connect("key_press_event", on_key)

# ----------------------------
# Simulation loop
# ----------------------------
while True:
    alpha = math.radians(alpha_deg)

    # --- Lift coefficient with stall ---
    if alpha_deg <= stall_angle_deg:
        CL = 2.5 * alpha
    else:
        CL = 2.5 * math.radians(stall_angle_deg) * 0.5  # lose lift after stall

    CD = 0.02 + 0.03 * (alpha ** 2)  # drag

    v = math.sqrt(vx**2 + vy**2)
    if v < 0.1:
        v = 0.1

    ux = vx / v
    uy = vy / v

    # Forces
    L = 0.5 * rho * v**2 * CL * A
    D = 0.5 * rho * v**2 * CD * A

    Fx_drag = -D * ux
    Fy_drag = -D * uy
    Fx_lift = -L * uy
    Fy_lift = L * ux

    Fx_total = Fx_drag + Fx_lift + T
    Fy_total = Fy_drag + Fy_lift - m * g

    ax_plane = Fx_total / m
    ay_plane = Fy_total / m

    vx += ax_plane * dt
    vy += ay_plane * dt
    x += vx * dt
    y += vy * dt

    if y <= 0:
        y = 0
        vy = 0

    # ---- Trail ----
    trail_x.append(x)
    trail_y.append(y)
    trail_line.set_data(trail_x, trail_y)

    # ---- Rotate airplane ----
    angle = math.degrees(math.atan2(vy, vx))
    theta = math.radians(angle)

    base_pts = [[-5, -2], [-5, 2], [10, 0]]
    rotated_pts = []
    for px, py in base_pts:
        rx = x + px * math.cos(theta) - py * math.sin(theta)
        ry = y + px * math.sin(theta) + py * math.cos(theta)
        rotated_pts.append([rx, ry])

    plane_shape.set_xy(rotated_pts)

    # ---- Stall warning ----
    if alpha_deg > stall_angle_deg:
        ax.set_title(f"STALL! AoA: {alpha_deg}°", color='red')
    else:
        ax.set_title(f"2D Flight Sim - AoA: {alpha_deg}°", color='black')

    plt.pause(0.01)
