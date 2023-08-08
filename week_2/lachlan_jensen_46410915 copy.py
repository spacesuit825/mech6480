import numpy as np
import matplotlib.pyplot as plt

num_volumes = 8

U_radial = 0
radius = 1
mu = 1
pressure_grad = -0.001

dr = radius / num_volumes

cell_dr = np.linspace(dr/2, radius - dr/2, num_volumes)

north_dr = np.linspace(dr, radius, num_volumes)
south_dr = np.linspace(0, radius - dr, num_volumes)

rhs = (1/mu) * pressure_grad * cell_dr * dr

m_diagl = -(north_dr + south_dr) / dr

l_diagl = south_dr[1:] / dr
r_diagl = north_dr[:-1] / dr

A = np.diag(m_diagl, 0) + np.diag(l_diagl, -1) + np.diag(r_diagl, 1)

A[-1, -1] = -(north_dr[-1] + south_dr[-1]) / (dr / 2)
A[-1, -2] = south_dr[-1] / dr

rhs[-1] -= ((north_dr[-1] / (dr / 2)) * U_radial)

A[0, 1] = north_dr[1] / dr
A[0, 0] = -north_dr[1] / dr

x = np.linalg.solve(A, rhs)




def exact_solution(radii: np.array) -> np.array:
    velocity = (1/(4*mu)) * pressure_grad * (radii**2 - radius**2)
    return velocity

def obtain_revision_number() -> str:
    repo = Repo('.', search_parent_directories=True)
    revsha = repo.head.object.hexsha[:8]
    
    return revsha

# Plotting the solutions
exact = exact_solution(cell_dr)
fig, ax = plt.subplots()

ax.plot(exact, cell_dr, color = 'r')
ax.plot(x, cell_dr, color = 'b', marker = '*')

plt.title(f"Pipe flow velocity distribution with {num_volumes} finite volumes")
plt.legend(["Exact Solution", "FVM Approximation"])
plt.xlabel("Velocity (m/s)")
plt.ylabel("Radial Distance (m)")
plt.ylim((0.0, 1.0))

# Add the timestamps and revision numbers
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ax.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)
ax.annotate(f"[rev {obtain_revision_number()}]", xy=(0.05,0.95), xycoords="figure fraction", annotation_clip=False)

# Set the grid such that it shows the cell boundaries
#ax.set_yticks(face_dr, minor=True)
#ax.grid(which = "minor", axis='y')

plt.show()
