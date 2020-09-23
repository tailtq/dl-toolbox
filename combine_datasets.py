import os
import glob
import shutil


def combine(directories, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    for index, directory in enumerate(directories):
        txt_links = glob.glob(directory + '/*.txt')

        for txt_link in txt_links:
            if txt_link.endswith('classes.txt'):
                continue

            filename = txt_link.split('/')[-1].split('.')[0]
            img_link = txt_link.split('.')[0] + '.jpg'
            new_txt_link = destination + str(index) + '_' + filename + '.txt'
            new_img_link = destination + str(index) + '_' + filename + '.jpg'

            shutil.copyfile(txt_link, new_txt_link)
            shutil.copyfile(img_link, new_img_link)


if __name__ == '__main__':
    destination = 'road_encroachment/'
    directories = ['data/GH010951_f', 'data/GH010952_f', 'data/GH010953_f', 'data/GH010954_f', 'data/GH010955', 'data/GH010956', 'data/GH011007', 'data/GH011008']
    combine(directories, destination)
