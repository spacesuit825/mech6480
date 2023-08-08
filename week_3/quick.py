import numpy as np
import matplotlib.pyplot as plt
from git import Repo
from datetime import datetime

n_sections = 16

length = 1

phi_L = 1
phi_R = 0

rho = 1.0 # kg/m3
gamma = 0.1 #kg/ms
u = 0.2 # m/s

dx = length / n_sections

centre_pos = np.linspace(dx/2, length - dx/2, n_sections)
face_pos = np.linspace(0, length, n_sections)

F = rho * u
D = gamma / dx

a_p = (D - (3/8) * F + D + (6/8) * F)
a_w = -(D + (6/8) * F + (1/8) * F)
a_e = -(D - (3/8) * F)
a_ww = (1/8) * F

m_diagl = np.full((n_sections), a_p)
rr_diagl = np.full((n_sections - 2), a_ww)
r_diagl = np.full((n_sections - 1,), a_w)
l_diagl = np.full((n_sections - 1,), a_e)

rhs = np.zeros((n_sections,))

rhs[0] = ((2/8) * F + F + (8/3) * D) * phi_L
rhs[1] = -(2/8) * F

A = np.diag(m_diagl, 0) + np.diag(l_diagl, 1) + np.diag(r_diagl, -1) + np.diag(rr_diagl, -2)

A[0, 0] = ((7/8) * F + D + (9/3) * D)
A[0, 1] = ((3/8) * F - D - (1/3) * D)

A[1, 0] = -(7/8) * F - (1/8) * F - D

A[-1, -1] = (-(3/8) * F + (9/3) * D + D)
A[-1, -2] = (-(6/8) * F - (1/3) * D - D)

def exact_soln(centre_pos: np.array) -> np.array:
    return phi_L + (phi_R - phi_L) * ((np.exp((rho * u * centre_pos)/gamma)-1) / (np.exp((rho * u * length)/gamma)-1))

def obtain_revision_number() -> str:
    repo = Repo('.', search_parent_directories=True)
    revsha = repo.head.object.hexsha[:8]
    
    return revsha

x = np.linalg.solve(A, rhs)

fig, ax = plt.subplots()

x_vals = np.linspace(0, 1, 100)

ax.plot(centre_pos, x, "b-*")
ax.plot(x_vals, exact_soln(x_vals), "r--")

plt.title(f"QUICK scheme for {n_sections} finite volumes")
plt.legend(["Exact Solution", "FVM Approximation"])
plt.xlabel("Concentration")
plt.ylabel("Distance (m)")
plt.ylim((-0.1, 1.1))

# Add the timestamps and revision numbers
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
ax.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)
ax.annotate(f"[rev {obtain_revision_number()}]", xy=(0.05,0.95), xycoords="figure fraction", annotation_clip=False)

plt.show()

