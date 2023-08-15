import numpy as np
import matplotlib.pyplot as plt

C_0 = 0.001 # kg/m3
D = 0.1 # m2/s
R_0 = 0.0425 #m3/s

A = 0.1 # m2

length = 20 # m
total_time = 3 * 60 * 60

n_cells = 20
time_between_plots = 540
dx = length / n_cells

x_locations = np.linspace(0.5 * dx, (n_cells - 0.5) * dx, n_cells)

dt = 0.2 # secs
plot_dt = time_between_plots / dt # secs
steps = int(total_time / dt) + 1

concentration = np.zeros(n_cells, dtype = float)
new_concentration = np.zeros(n_cells, dtype = float)

fig, ax = plt.subplots(1, 2, subplot_kw = dict(box_aspect = 1))

plot_ls = []
n_plots = int(total_time / time_between_plots)

time = 0
for step in range(steps):
    time += dt

    # Internal
    for cell in range(1, n_cells - 1):
        new_concentration[cell] = concentration[cell] + ((D * dt) / dx**2) * (concentration[cell + 1] - 2 * concentration[cell] + concentration[cell - 1])
        #print(new_concentration)

    new_concentration[0] = concentration[0] + ((D * dt / dx**2) * (concentration[1] - concentration[0]) + ((C_0 * R_0 * dt) / A))
    #concentration[0] - (dt / dx) * (((C_0 * R_0) / A) + (1 / dx) * (concentration[1] - concentration[0])))
    new_concentration[-1] = concentration[-1] + (dt / dx) * ((-R_0 / A) * ((3/2) * concentration[-1] - (1/2) * concentration[-2]) - (D / dx) * (concentration[-1] - concentration[-2]))

    concentration[:] = new_concentration[:]

    if step % plot_dt == 0:
        plot_ls.append(concentration.copy())


def analytical(x_arr: np.array) -> np.array:
    return C_0 + C_0 * R_0 * ((length - x_arr) / (D * A))

print(len(plot_ls))
for plot in range(n_plots):

    if plot != n_plots - 1:
        ax[0].plot(x_locations, plot_ls[plot], "k--")
    else:
        ax[0].plot(x_locations, plot_ls[plot], "b*")

ax[0].plot(x_locations, analytical(x_locations), "r")

def computeConcentrations(x_locations, plot_ls) -> np.array:
    tot_concent = []
    for plot in range(len(plot_ls) - 1):
        sum = 0.0
        for loc in range(len(x_locations)):
            sum += plot_ls[plot][loc] * dx

        sum *= A
        tot_concent.append(sum)

    return np.array(tot_concent)

time_arr = np.linspace(0, total_time, n_plots)
ax[1].plot(time_arr, computeConcentrations(x_locations, plot_ls))


plt.show()
