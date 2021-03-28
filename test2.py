# import cv2
# import glob
# import os
#
#
# directory = "unlabelled-real-cases"
# files = sorted(glob.glob(f"{directory}/*_ignore.txt"))
#
# for file in files:
#     real_file = file.replace("_ignore", "")
#
#     ignored_content = open(file, "r").read()
#
#     if os.path.exists(real_file):
#         open(real_file, "a").write(ignored_content)
#     # lines = open(file, "r").readlines()
#     # lines = list(filter(lambda line: line[0] == "2", lines))
#     # if len(lines) == 0:
#     #     os.remove(file)
#     # else:
#     #     open(file, "w").write("".join(lines))
#     # print(len(lines))
#


import cv2
import glob
import os
import shutil


directory = "/Users/tailtq/Downloads/test"
files = sorted(glob.glob(f"{directory}/*.jpg"))

for file in files:
    file_name = file.split("/")[-1].split(".")[0]
    txt_path = file.replace("jpg", "txt")

    new_file_name = file_name.rjust(5, "0")

    new_path = "/".join(file.split("/")[:-1])
    new_img_path = f"{new_path}/{new_file_name}.jpg"
    new_txt_path = f"{new_path}/{new_file_name}.txt"

    shutil.move(file, new_img_path)
    shutil.move(txt_path, new_txt_path)
    print(new_path)
