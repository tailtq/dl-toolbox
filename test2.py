import cv2
import glob
import os


directory = "unlabelled-real-cases"
files = sorted(glob.glob(f"{directory}/*_ignore.txt"))

for file in files:
    real_file = file.replace("_ignore", "")

    ignored_content = open(file, "r").read()

    if os.path.exists(real_file):
        open(real_file, "a").write(ignored_content)
    # lines = open(file, "r").readlines()
    # lines = list(filter(lambda line: line[0] == "2", lines))
    # if len(lines) == 0:
    #     os.remove(file)
    # else:
    #     open(file, "w").write("".join(lines))
    # print(len(lines))

