# Lachlan Jensen 46410915

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import os

def load_data(filepath: set) -> np.array:
    out = []
    # check filepath is valid

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

            # Assume all other lines have the shape [float, ' ', float]
            x_value = float(tokenised_line[0])
            y_value = float(tokenised_line[2])

            out.append([x_value, y_value])

    return np.array(out)

def plot_graph(array: np.array, labels: list) -> None:
    fig, ax = plt.subplots()
    ax.plot(array[:, 0], array[:, 1])
    plt.title(labels[0])
    plt.xlabel(labels[1])
    plt.ylabel(labels[2])

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ax.annotate(timestamp, xy=(0.7,0.95), xycoords="figure fraction", annotation_clip=False)

    plt.show()

out = load_data("C:/Users/lachl/OneDrive/Documents/python/mech6480/week_1/data/curve.data")
plot_graph(out, ["Test Plot", "x", "f(x)"])



