import glob
import os
import random
import shutil
from compare_two_directories import get_all_images

random.seed(3)


def remove_files_from_total(total_files, removed_files):
    return [file for file in total_files if file not in removed_files]


def move_files(files, destination):
    destination += '/'

    for file in files:
        file_name = file.split('.')[0]
        # xml_file = file_name + '.xml'
        txt_file = file_name + '.txt'

        shutil.move(file, destination)
        # shutil.move(xml_file, destination)
        shutil.move(txt_file, destination)


def separate_dataset(files, total, percent, destination):
    random_length = round(total * percent)
    random_files = random.sample(files, k=random_length)
    files = remove_files_from_total(files, random_files)
    move_files(random_files, destination)

    return files


if __name__ == '__main__':
    training_percent = 0.8
    val_percent = 0.2
    test_percent = 0.0

    directory = 'road_encroachment'
    training_set_dir = 'data/dataset/training_set'
    val_set_dir = 'data/dataset/val_set'
    test_set_dir = 'test_set'

    if round(training_percent + val_percent + test_percent, 5) != 1:
        print('Invalid percentages')
        exit()

    if not os.path.exists(val_set_dir):
        os.mkdir(val_set_dir)

    if not os.path.exists(test_set_dir) and test_percent != 0:
        os.mkdir(test_set_dir)

    files = get_all_images(directory)
    total = len(files)

    files = separate_dataset(files, total, val_percent, val_set_dir)
    files = separate_dataset(files, total, test_percent, test_set_dir)

    if not os.path.exists(training_set_dir):
        os.rename(directory, training_set_dir)
