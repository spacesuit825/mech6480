import numpy as np
import matplotlib.pyplot as plt

# nodes x nodes = A
# nodes = x
# nodes = RHS

diffusivity = 1000

class Cell:
    def __init__(self, i, j, diffusivity, dx, dy):
        self.i = i
        self.j = j
        self.diff = diffusivity
        self.dx = dx
        self.dy = dy

    def compute_cell(self):
        a_w = (self.diff * self.dy) / (self.dx / 2)
        a_e = (self.diff * self.dy) / (self.dx / 2)
        a_n = (self.diff * self.dx) / (self.dy / 2)
        a_s = (self.diff * self.dx) / (self.dy / 2)

        a_p = a_w + a_e + a_s + a_n

        return np.array([a_p, a_w, a_e, a_n, a_s])

class Domain:
    def __init__(self, bounds, dx, dy):
        self.bounds = bounds # [[x, y], [x, y]]
        self.dx = dx
        self.dy = dy
        self.n_nodes = bounds[1][0] - bounds[0][0]
        self.cells = []
        self.domain = np.zeros((self.n_nodes, self.n_nodes))

    def init_cells(self):
        for i in range(self.n_nodes):
            for j in range(self.n_nodes):
                self.domain.append(Cell(i, j, 1000, self.dx, self.dy))

    def assemble_A_matrix(self):
        for i in range(self.n_nodes):
            x = i / self.n_nodes
            y = i % self.n_nodes

            
        