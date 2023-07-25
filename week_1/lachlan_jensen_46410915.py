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

def plot_graph(ls: list, labels: list = ["sin(x)", "x", "f(x)"]) -> None:
    fig, ax = plt.subplots()

    # Add each plot to the axes object (for later tasks)
    for array in ls:
        ax.plot(array[:, 0], array[:, 1])

    # Add the specified labels
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])

    plt.grid()

    plt.show()

out = load_data("C:/Users/lachl/OneDrive/Documents/python/mech6480/week_1/data/curve.data")
plot_graph([out])