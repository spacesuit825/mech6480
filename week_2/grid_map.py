import numpy as np

grid_origin = (0, 0, 0)

grid_upper = (1, 1, 1)
grid_lower = (0, 0, 0)

n_cells = 2

lower_bound = [(0.05, 0.05, 0.05)]
upper_bound = [(0.45, 0.45, 0.45)]

cells = {}

def map_to_grid(lower_b, upper_b, grid_upper, grid_lower, n_cells, grid_origin, cells):

    grid_coords_upper = (n_cells, n_cells, n_cells)
    grid_coords_lower = (0, 0, 0)

    cell_size = (grid_upper[0] - grid_lower[0]) / n_cells

    print(cell_size)
    
    for n, obj in enumerate(lower_b):
        print((upper_b[n][0] - grid_origin[0]) / cell_size)
        lower_x = np.floor((obj[0] - grid_origin[0]) / cell_size).astype(int)
        lower_y = np.floor((obj[1] - grid_origin[1]) / cell_size).astype(int)
        lower_z = np.floor((obj[2] - grid_origin[2]) / cell_size).astype(int)

        upper_x = np.ceil((upper_b[n][0] - grid_origin[0]) / cell_size).astype(int)
        upper_y = np.ceil((upper_b[n][1] - grid_origin[1]) / cell_size).astype(int)
        upper_z = np.ceil((upper_b[n][2] - grid_origin[2]) / cell_size).astype(int)

        for x in range(lower_x, upper_x):
            for y in range(lower_y, upper_y):
                for z in range(lower_z, upper_z):
                    idx = (z * n_cells * n_cells) + (y * n_cells) + x
                    cells[idx] = n

        return cells
    
cells = map_to_grid(lower_bound, upper_bound, grid_upper, grid_lower, n_cells, grid_origin, cells)

for cell_coords, obj_indices in cells.items():
    print(f"Cell {cell_coords}: Objects {obj_indices}")