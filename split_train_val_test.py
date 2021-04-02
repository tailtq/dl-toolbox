import glob
import os
import random
import shutil
from compare_two_directories import get_all_images

random.seed(3)


def remove_files_from_total(total_files, removed_files):
    return [file for file in total_files if file not in removed_files]


def move_files(files, destination):
    destination += "/"

    for file in files:
        file_name = file.split(".")[0]
        # xml_file = file_name + ".xml"
        txt_file = file_name + ".txt"

        shutil.move(file, destination)
        # shutil.move(xml_file, destination)
        shutil.move(txt_file, destination)


def separate_dataset(files, total, percent, destination):
    random_length = round(total * percent)
    random_files = random.sample(files, k=random_length)
    files = remove_files_from_total(files, random_files)
    move_files(random_files, destination)

    return files


if __name__ == "__main__":
    training_percent = 0.8
    val_percent = 0.2
    test_percent = 0.0

    directory = "original-dataset-should-save"
    patterns = [
        f"{directory}/273271,*.jpg",
        f"{directory}/mak*.png",
        f"{directory}/custom_atai*.png",
        f"{directory}/custom_qtai*.png",
        f"{directory}/custom_qtai*.jpeg",
        f"{directory}/custom_qtai*.jpg",
        f"{directory}/custom_cctv1*.jpg",
        f"{directory}/custom_cctv2*.jpg",
        f"{directory}/custom_cctv3*.jpg",
        f"{directory}/custom_cctv4*.jpg",
        f"{directory}/*.jpg",
    ]

    training_set_dir = "dataset/train"
    val_set_dir = "dataset/val"
    test_set_dir = "dataset/test"

    if round(training_percent + val_percent + test_percent, 5) != 1:
        print("Invalid percentages")
        exit()

    if not os.path.exists(training_set_dir):
        os.mkdir(training_set_dir)

    if not os.path.exists(val_set_dir):
        os.mkdir(val_set_dir)

    if not os.path.exists(test_set_dir) and test_percent != 0:
        os.mkdir(test_set_dir)

    for pattern in patterns:
        files = sorted(glob.glob(pattern))
        total = len(files)

        files = separate_dataset(files, total, val_percent, val_set_dir)
        files = separate_dataset(files, total, test_percent, test_set_dir)

        files = glob.glob(pattern)
        move_files(files, training_set_dir)
