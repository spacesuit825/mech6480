import numpy as np
import matplotlib.pyplot as plt
from pyevtk.hl import gridToVTK

Lx = 10.0 # m
Ly = 10.0 # m
alpha = 4.0 # Diffusivity coeff

## GRID
nx = 21
ny = 21
dx = Lx / nx # m
dy = Ly / ny # m

## TIME
time = 0.0 # secs
dt = 6.25e-3 # secs
time_end = 62.5e-1

plotting = 10

T_cool = 300.0
T_hot = 700.0
T_wall_t = 350
T_wall_r = 400

S = -2000

x = np.linspace(dx/2, Lx - dx/2, nx)
y = np.linspace(dy/2, Ly - dy/2, ny)

X, Y = np.meshgrid(x, y, indexing = "ij")

T = np.ones((nx, ny)) * T_cool

x_flux = np.zeros((nx + 1, ny))
y_flux = np.zeros((nx, ny + 1))

r, cx, cy = 2, 5, 5
r2 = r**2

# # Initial conditions
# for i in range(nx):
#     for j in range(ny):
#         p2 = (x[i] - cx)**2 + (y[j] - cy)**2
#         if p2 < r2:
#             T[i, j] = T_hot

fig, ax = plt.subplots(1, 1)
#ax.contourf(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot")
cbar = fig.colorbar(ax.contourf(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot"))

plot_counter = 0
while time < time_end:
    time += dt

    x_flux[1:-1, :] = -alpha * (T[1:, :] - T[:-1, :]) / dx
    y_flux[:, 1:-1] = -alpha * (T[:, 1:] - T[:, :-1]) / dy

    x_flux[0, :] = -alpha * (T[0, :] - T_wall_r) / (dx / 2.0)
    x_flux[-1, :] = 0

    y_flux[:, 0] = 0
    y_flux[:, -1] = -alpha * (T_wall_t - T[:, -1]) / (dx / 2.0)

    x_flux[int(np.floor(nx/2)), int(np.floor(nx/2))] += S * dx * dy
    y_flux[int(np.floor(ny/2)), int(np.floor(ny/2))] += S * dx * dy

    T = T - (dt / (dx * dy)) * (dy * (x_flux[1:, :] - x_flux[:-1, :]) + dx * (y_flux[:, 1:] - y_flux[:, :-1]) / dy)

    # Comment this out of part 2
    T[int(np.floor(nx/2)), int(np.floor(ny/2))] += S * dt

    if plot_counter % plotting == 0:
        cbar.remove()
        ax.cla()
        con = ax.contourf(X, Y, T, vmin = T_cool, vmax = T_hot, cmap = "hot", levels = 15)
        cbar = fig.colorbar(con)
        ax.set_aspect("equal")

        vtk_x = np.linspace(0, Lx, nx + 1)
        vtk_y = np.linspace(0, Ly, ny + 1)

        no_slices = 1

        vtk_z = np.arange(0, no_slices + 1) * dx
        vtk_temp = np.dstack([T] * no_slices)

        gridToVTK("C:/Users/lachl/OneDrive/Documents/python/mech6480/week_5/data/temperature" + str(plot_counter).zfill(8), vtk_x, vtk_y, vtk_z, cellData = {"temp": vtk_temp})

        # ax[1].cla()
        # ax[1].plot(T[int(nx / 2), :], y)
        plt.pause(0.001)
    plot_counter += 1
plt.show()