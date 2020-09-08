import glob
import os
import random
import shutil


def remove_files_from_total(total_files, removed_files):
    return [file for file in total_files if file not in removed_files]


def move_files(files, destination):
    destination += '/'

    for file in files:
        file_name = file.split('.')[0]
        xml_file = file_name + '.xml'
        txt_file = file_name + '.txt'

        shutil.move(file, destination)
        shutil.move(xml_file, destination)
        shutil.move(txt_file, destination)


def separate_dataset(files, total, percent, destination):
    test_set_length = round(total * percent)
    test_files = random.sample(files, k=test_set_length)
    files = remove_files_from_total(files, test_files)
    move_files(test_files, destination)

    return files


if __name__ == '__main__':
    training_percent = 0.7
    val_percent = 0.2
    test_percent = 0.1

    directory = 'training_set'
    training_set_dir = 'training_set'
    val_set_dir = 'val_set'
    test_set_dir = 'test_set'

    if round(training_percent + val_percent + test_percent, 5) != 1:
        print('Invalid percentages')
        exit()

    if not os.path.exists('training_set'):
        os.mkdir('training_set')

    if not os.path.exists('val_set'):
        os.mkdir('val_set')

    if not os.path.exists('test_set'):
        os.mkdir('test_set')

    files = glob.glob('{}/*.JPG'.format(directory))
    total = len(files)

    files = separate_dataset(files, total, val_percent, val_set_dir)
    files = separate_dataset(files, total, test_percent, test_set_dir)
