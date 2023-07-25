# Lachlan Jensen 46410915

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

from git import Repo

import os

def load_data(filepath: set) -> np.array:
    # Intermediate storage for the coordinates
    out = []

    # load file
    with open(filepath) as f:
        lines = f.readlines()

        for line in lines:
            # Remove whitespace (\n, etc.)
            stripped_line = line.strip()
            # Split the line into tokens
            tokenised_line = stripped_line.split(' ')

            # Skip any comments
            if tokenised_line[0] == "#":
                continue

            # Assume all other lines have the shape [str, ' ', str]
            x_value = float(tokenised_line[0]) # <-- Use float() to convert from the str to float type
            y_value = float(tokenised_line[2])

            out.append([x_value, y_value])

    # Convert to numpy type
    return np.array(out)

def compute_central_difference(input_array: np.array) -> list[np.array]:
    out = []
    out_error = []

    num_points = input_array.shape[0]
    for row in range(num_points):
        if row == 0 or row == num_points - 1:
            continue

        h = input_array[row + 1, 0] - input_array[row, 0]
        f_dash = (input_array[row + 1, 1] - input_array[row - 1, 1]) / (2 * h)

        error = np.cos(input_array[row, 0]) - f_dash

        out.append([input_array[row, 0], f_dash])
        out_error.append([input_array[row, 0], error])

    return [np.array(out), np.array(out_error)]

def compute_forward_difference(input_array: np.array) -> list[np.array]:
    out = []
    out_error = []

    num_points = input_array.shape[0]
    for row in range(num_points):
        if row == num_points - 1:
            continue

        h = input_array[row + 1, 0] - input_array[row, 0]
        f_dash = (input_array[row + 1, 1] - input_array[row, 1]) / (h)

        error = np.cos(input_array[row, 0]) - f_dash

        out.append([input_array[row, 0], f_dash])
        out_error.append([input_array[row, 0], error])

    return [np.array(out), np.array(out_error)]

def obtain_revision_number() -> str:
    repo = Repo('.', search_parent_directories=True)
    revsha = repo.head.object.hexsha[:8]
    
    return revsha

def plot_graph(ls: list, labels: list) -> None:
    fig, ax = plt.subplots()

    # Add each plot to the axes object
    for array in ls:
        ax.plot(array[:, 0], array[:, 1])

    # Add the specified labels
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])

    # Add the timestamps, and revision numbers
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)
    ax.annotate(f"[rev {obtain_revision_number()}]", xy=(0.05,0.95), xycoords="figure fraction", annotation_clip=False)

    plt.show()

out = load_data("C:/Users/lachl/OneDrive/Documents/python/mech6480/week_1/data/curve.data")
d_central_out = compute_central_difference(out)
d_forward_out = compute_forward_difference(out)
plot_graph([out, d_central_out[0], d_forward_out[0]], ["Test Plot", "x", "f(x)"])
print(d_central_out[1])
plot_graph([d_central_out[1], d_forward_out[1]], ["Test Plot", "x", "error"])



