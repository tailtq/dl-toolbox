import cv2
import glob
import os
import numpy as np

directory = "data/trim_2"
files = sorted(glob.glob(f"{directory}/*.txt"))

# Define ignored regions
IGNORED_AREAS_ORIGIN = np.array([
    [3, 0.909697, 0.239103, 0.075152, 0.178205],
    [3, 0.831515, 0.719872, 0.236364, 0.552564],
])
IGNORED_AREAS = np.copy(IGNORED_AREAS_ORIGIN)
IGNORED_AREAS[:, 1] = IGNORED_AREAS[:, 1] - IGNORED_AREAS[:, 3] / 2
IGNORED_AREAS[:, 2] = IGNORED_AREAS[:, 2] - IGNORED_AREAS[:, 4] / 2
IGNORED_AREAS[:, 3] = IGNORED_AREAS[:, 1] + IGNORED_AREAS[:, 3]
IGNORED_AREAS[:, 4] = IGNORED_AREAS[:, 2] + IGNORED_AREAS[:, 4]

IGNORED_AREAS_STRING = IGNORED_AREAS_ORIGIN.tolist()

for i, IGNORED_AREAS_ELEMENT in enumerate(IGNORED_AREAS_STRING):
    IGNORED_AREAS_ELEMENT[0] = int(IGNORED_AREAS_ELEMENT[0])
    IGNORED_AREAS_ELEMENT = [str(e) for e in IGNORED_AREAS_ELEMENT]
    IGNORED_AREAS_STRING[i] = " ".join(IGNORED_AREAS_ELEMENT) + "\n"

for file in files:
    if file == f"{directory}/classes.txt":
        continue

    print(file)
    lines = open(file, "r").readlines()

    ignored_area_lines = list(filter(lambda line: line[0] == "3", lines))
    removed_indices = []

    for index, line in enumerate(lines):
        if line[0] == "3":
            continue

        segments = line.split(" ")
        coordinates = [float(segment) for segment in segments[1:5]]
        coordinates = [
            coordinates[0] - coordinates[2] / 2,
            coordinates[1] - coordinates[3] / 2,
            coordinates[0] + coordinates[2] / 2,
            coordinates[1] + coordinates[3] / 2,
        ]

        # Filter regions inside these ignored regions
        for area_coordinates in IGNORED_AREAS:
            if (coordinates[0] >= area_coordinates[1]
                    and coordinates[1] >= area_coordinates[2]
                    and coordinates[2] <= area_coordinates[3]
                    and coordinates[3] <= area_coordinates[4]):
                removed_indices.append(index)

    for index in sorted(removed_indices, reverse=True):
        del lines[index]

    lines.extend(IGNORED_AREAS_STRING)
    print(IGNORED_AREAS_STRING)

    open(file, "w").write("".join(lines))
