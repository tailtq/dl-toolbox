import cv2
import glob
import os


directory = "unlabelled-real-cases"
files = sorted(glob.glob(f"{directory}/*.txt"))

for file in files:
    if file == "unlabelled-real-cases/classes.txt":
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

        for ignored_area_line in ignored_area_lines:
            segments = ignored_area_line.split(" ")
            area_coordinates = [float(segment) for segment in segments[1:5]]
            area_coordinates = [
                area_coordinates[0] - area_coordinates[2] / 2,
                area_coordinates[1] - area_coordinates[3] / 2,
                area_coordinates[0] + area_coordinates[2] / 2,
                area_coordinates[1] + area_coordinates[3] / 2,
            ]

            if (coordinates[0] >= area_coordinates[0]
                and coordinates[1] >= area_coordinates[1]
                and coordinates[2] <= area_coordinates[2]
                and coordinates[3] <= area_coordinates[3]):
                removed_indices.append(index)

                print(coordinates, area_coordinates)

    for index in sorted(removed_indices, reverse=True):
        print(index, len(lines))
        del lines[index]

    open(file, "w").write("".join(lines))
