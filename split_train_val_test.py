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


def move_bias_files(file_names, directory, train_dir):
    for file_name in file_names:
        for extension in ["jpg", "jpeg", "png"]:
            file = f"{directory}/{file_name}.{extension}"

            if os.path.exists(file):
                shutil.move(file, train_dir)

        txt_file = f"{directory}/{file_name}.txt"

        if os.path.exists(txt_file):
            shutil.move(txt_file, train_dir)
        else:
            print(f"{txt_file}: File doesn't exist")


if __name__ == "__main__":
    training_percent = 0.8
    val_percent = 0.2
    test_percent = 0.0

    directory = "oke"
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
    bias_files = [
        "custom_qtai_2306",
        "custom_qtai_3321",
        "custom_qtai_3510",
        "custom_qtai_3695",
        "custom_qtai_3735",
        "custom_qtai_3788",
        "custom_qtai_3811",
        "custom_qtai_3814",
        "custom_qtai_3817",
        "custom_qtai_3858",
        "custom_qtai_3863",
        "custom_qtai_3899",
        "custom_qtai_3939",
        "custom_qtai_3960",
        "custom_qtai_3972",
        "custom_qtai_3980",
        "custom_qtai_4017",
        "custom_qtai_4039",
        "custom_qtai_4171",
        "custom_qtai_4203",
        "custom_qtai_4205",
        "custom_qtai_4243",
        "custom_qtai_4280",
        "custom_qtai_4355",
        "custom_qtai_4356",
        "custom_qtai_4446",
        "custom_qtai_4507",
        "custom_qtai_4556",
        "custom_qtai_4601",
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

    move_bias_files(bias_files, directory, training_set_dir)

    for pattern in patterns:
        files = sorted(glob.glob(pattern))
        total = len(files)

        files = separate_dataset(files, total, val_percent, val_set_dir)
        files = separate_dataset(files, total, test_percent, test_set_dir)

        files = glob.glob(pattern)
        move_files(files, training_set_dir)
