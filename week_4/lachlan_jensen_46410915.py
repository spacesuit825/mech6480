import numpy as np
import matplotlib.pyplot as plt
from git import Repo
from datetime import datetime

C_0 = 0.001 # kg/m3
D = 0.1 # m2/s
R_0 = 0.0425 #m3/s

A = 0.1 # m2

length = 20 # m
total_time = 3 * 60 * 60 # secs = 10800

n_cells = 20
time_between_plots = 540 # secs
dx = length / n_cells

x_locations = np.linspace(0.5 * dx, (n_cells - 0.5) * dx, n_cells)

dt = 0.2 # secs
plot_dt = time_between_plots / dt # timesteps
steps = int(total_time / dt) + 1

# Concentration array with temp new_concentration
concentration = np.zeros(n_cells, dtype = float)
new_concentration = np.zeros(n_cells, dtype = float)

fig, ax = plt.subplots(1, 2)#, subplot_kw = dict(box_aspect = 1))

# Keep track of each concentration array so they can be plotted later
plot_ls = []

time = 0
for step in range(steps):
    time += dt

    # Compute new concentration (don't worry about the wrapping due to np.roll, those are overwritten by the B.C.s)
    new_concentration = concentration + ((D * dt) / dx**2) * (np.roll(concentration, 1) - 2 * concentration + np.roll(concentration, -1))
    
    # Boundary Conditions (overwrite the end values)
    new_concentration[0] = concentration[0] + ((D * dt / dx**2) * (concentration[1] - concentration[0]) + ((C_0 * R_0 * dt) / A))
    new_concentration[-1] = concentration[-1] + (dt / dx) * ((-R_0 / A) * ((3/2) * concentration[-1] - (1/2) * concentration[-2]) - (D / dx) * (concentration[-1] - concentration[-2]))

    concentration[:] = new_concentration[:]

    if step % plot_dt == 0:
        # Perform a deep copy of the concentration array so it isnt overwritten on later updates
        plot_ls.append(concentration.copy())

def analytical(x_arr: np.array) -> np.array:
    return C_0 + C_0 * R_0 * ((length - x_arr) / (D * A))

def computeConcentrations(x_locations: np.array, plot_ls: list) -> np.array:
    tot_concent = []
    for plot in range(len(plot_ls)):
        integral = 0.0
        for loc in range(len(x_locations)):
            integral += plot_ls[plot][loc] * dx

        integral *= A
        tot_concent.append(integral)
    return np.array(tot_concent)

def obtain_revision_number() -> str:
    repo = Repo('.', search_parent_directories=True)
    revsha = repo.head.object.hexsha[:8]
    
    return revsha

# Plot the different concentration distributions
for plot in range(len(plot_ls)):

    if plot != len(plot_ls) - 1:
        ax[0].plot(x_locations, plot_ls[plot], "k--")
    else:
        ax[0].plot(x_locations, plot_ls[plot], "b*")

ax[0].plot(x_locations, analytical(x_locations), "r")
ax[0].set_title("Concentration Distributions")
ax[0].set_xlabel("Position (m)")
ax[0].set_ylabel("Concentration (kg/m3)")


time_arr = np.linspace(0, total_time, len(plot_ls))
ax[1].plot(time_arr, computeConcentrations(x_locations, plot_ls))
ax[1].set_title("Total Concentration with Time")
ax[1].set_xlabel("Time (secs)")
ax[1].set_ylabel("Total Concentration (kg/m3)")

# Set plot super title
plt.suptitle("Concentration Diffusion over Time")

# Add the timestamps and revision numbers
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
plt.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)
plt.annotate(f"[rev {obtain_revision_number()}]", xy=(0.05,0.95), xycoords="figure fraction", annotation_clip=False)

plt.subplots_adjust(hspace=0.5)
fig.set_size_inches(11, 5)

plt.show()
