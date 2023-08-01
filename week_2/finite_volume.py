import numpy as np
import matplotlib.pyplot as plt

diffusivity = 1000 # Wm/k
T_a = 100 # K
T_b = 500 # K

length = 0.5
n_sections = 5

dx = length / n_sections

a_star = (((2 * diffusivity) / dx) + (diffusivity / dx))
a_e = (diffusivity / dx)
a_w = (diffusivity / dx)
s_u = ((2 * diffusivity) / dx)

m_diag = []
l_diag = []
r_diag = []
rhs = []

# Assemble main diagonal
for n in range(n_sections):
    if n == 0:
        m_diag.append(-a_star)
    elif n == n_sections - 1:
        m_diag.append(-a_star)
    else:
        m_diag.append(-(a_e + a_w))

# Assemvle left diagonal
for n in range(n_sections - 1):
    l_diag.append(a_w)

# Assemble right diagonal
for n in range(n_sections - 1):
    r_diag.append(a_e)

# Assemble matrix
A = np.diag(m_diag, 0) + np.diag(l_diag, -1) + np.diag(r_diag, 1)

# Assemble RHS
for n in range(n_sections):
    if n == 0:
        rhs.append(-s_u * T_a)
    elif n == n_sections - 1:
        rhs.append(-s_u * T_b)
    else:
        rhs.append(0)

rhs = np.array(rhs)

x = np.linalg.solve(A, rhs)

print(x)