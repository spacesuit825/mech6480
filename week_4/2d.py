import numpy as np
import matplotlib.pyplot as plt

Lx = 10.0 # m
Ly = 10.0 # m
alpha = 4.0 # Diffusivity coeff

## GRID
nx = 101
ny = 101
dx = Lx / nx # m
dy = Ly / ny # m

## TIME
time = 0.0 # secs
dt = 6.25e-5 # secs
time_end = 62.5e-3

plotting = 10

T_cool = 300.0
T_hot = 700.0
T_wall = T_cool

x = np.linspace(dx/2, Lx - dx/2, nx)
y = np.linspace(dy/2, Ly - dy/2, ny)

X, Y = np.meshgrid(x, y, indexing = "ij")

T = np.ones((nx, ny)) * T_cool

x_flux = np.zeros((nx + 1, ny))
y_flux = np.zeros((nx, ny + 1))

r, cx, cy = 2, 5, 5
r2 = r**2

# Initial conditions
for i in range(nx):
    for j in range(ny):
        p2 = (x[i] - cx)**2 + (y[j] - cy)**2
        if p2 < r2:
            T[i, j] = T_hot

fig, ax = plt.subplots(1, 2)
# ax.contour(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot")
# cbar = fig.colorbar(ax.contour(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot"))

plot_counter = 0
while time < time_end:
    time += dt

    x_flux[1:-1, :] = -alpha * (T[1:, :] - T[:-1, :]) / dx
    y_flux[:, 1:-1] = -alpha * (T[:, 1:] - T[:, :-1]) / dy

    x_flux[0, :] = -alpha * (T[0, :] - T_wall) / (dx / 2.0)
    x_flux[-1, :] = -alpha * (T_wall - T[-1, :]) / (dx / 2.0)

    y_flux[:, 0] = -alpha * (T[:, 0] - T_wall) / (dx / 2.0)
    y_flux[:, -1] = -alpha * (T_wall - T[:, -1]) / (dx / 2.0)

    T = T - (dt / (dx * dy)) * (dy * (x_flux[1:, :] - x_flux[:-1, :]) + dx * (y_flux[:, 1:] - y_flux[:, :-1]) / dy)

    if plot_counter % plotting == 0:
        ax[0].cla()
        ax[0].contourf(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot")
        ax[0].set_aspect("equal")
        ax[1].cla()
        ax[1].plot(T[int(nx / 2), :], y)
        plt.pause(0.001)
    plot_counter += 1
plt.show()