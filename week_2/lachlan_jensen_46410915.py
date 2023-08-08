import numpy as np
import matplotlib.pyplot as plt
from git import Repo
from datetime import datetime

n_sections = 30 # or number of volumes. As n_sections -> oo, the approximation approaches the exact solution.

# Constants
U_r = 0 # m/s - No slip
radius = 1 # m
mu = 1 # Pa.s
p_grad = -0.001 # Pa/m

dr = radius / n_sections

# Simple Cell Layout
# r_n -----     - Northern boundary
#       N
# r_n ----- r_s
#       P
# r_n ----- r_s
#       S
#     ----- r_s - Southern boundary

# Cell-centered positions
centre_dr = np.linspace(dr/2, radius - dr/2, n_sections)
# Face-centred positions
face_dr = np.linspace(0, radius, n_sections + 1)

# Vectorised calculation for the RHS
rhs = (1/mu) * p_grad * centre_dr * dr

# Add the north and south faces and find a_p. Stagger the addition using np.roll and neglect the wrapped entry in the 0 position
m_diagl = -(np.roll(face_dr, 1) + face_dr)[1:] / dr


# Use the internal faces to find the off-diagonals
l_diagl = face_dr[1:-1] / dr
r_diagl = face_dr[1:-1] / dr

# Assemble the global/A matrix
global_matrix = np.diag(m_diagl, 0) + np.diag(l_diagl, -1) + np.diag(r_diagl, 1)

# Correct the top of the pipe (Dirchlet)
global_matrix[-1, -1] = -(face_dr[-1] + face_dr[-2]) / (dr / 2)
global_matrix[-1, -2] = face_dr[-2] / dr
# Adjust the RHS for the Dirchlet condition
rhs[-1] -= ((face_dr[-1] / (dr / 2)) * U_r)

# Correct the middle of the pipe (Neumann)
global_matrix[0, 0] = -face_dr[1] / dr
global_matrix[0, 1] = face_dr[1] / dr

# Solve the system
x = np.linalg.solve(global_matrix, rhs)

def exact_solution(radii: np.array) -> np.array:
    velocity = (1/(4*mu)) * p_grad * (radii**2 - radius**2)
    return velocity

def obtain_revision_number() -> str:
    repo = Repo('.', search_parent_directories=True)
    revsha = repo.head.object.hexsha[:8]
    
    return revsha

# Plotting the solutions
exact = exact_solution(centre_dr)
fig, ax = plt.subplots()

ax.plot(exact, centre_dr, color = 'r')
ax.plot(x, centre_dr, color = 'b', marker = '*')

plt.title(f"Pipe flow velocity distribution with {n_sections} finite volumes")
plt.legend(["Exact Solution", "FVM Approximation"])
plt.xlabel("Velocity (m/s)")
plt.ylabel("Radial Distance (m)")
plt.ylim((0.0, 1.0))

# Add the timestamps and revision numbers
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ax.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)
ax.annotate(f"[rev {obtain_revision_number()}]", xy=(0.05,0.95), xycoords="figure fraction", annotation_clip=False)

# Set the grid such that it shows the cell boundaries
ax.set_yticks(face_dr, minor=True)
ax.grid(which = "minor", axis='y')

plt.show()
