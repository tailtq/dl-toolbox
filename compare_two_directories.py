import glob
import cv2
import numpy as np
from PIL import Image


def dhash(image, hash_size=8):
    # resize the input image, adding a single column (width) so we
    # can compute the horizontal gradient
    resized = cv2.resize(image, (hash_size + 1, hash_size))
    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]
    # convert the difference image to a hash
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def get_hash(link):
    image = cv2.imread(link, cv2.IMREAD_GRAYSCALE)
    return dhash(image, 10)


def get_all_images(directory):
    formats = ['jpg', 'jpeg', 'JPG', 'JPEG', 'png', 'PNG']
    links = []

    for format in formats:
        links.extend(glob.glob('{}/*.{}'.format(directory, format)))

    return links


def find_matching_index(list1, list2):
    inverse_index = {element: index for index, element in enumerate(list1)}

    return [(index, inverse_index[element])
            for index, element in enumerate(list2) if element in inverse_index]


def nrmse(im1, im2):
    a, b = im1.shape[:2]
    rmse = np.sqrt(np.sum((im2 - im1) ** 2) / float(a * b))
    max_val = max(np.max(im1), np.max(im2))
    min_val = min(np.min(im1), np.min(im2))

    return 1 - (rmse / (max_val - min_val))


if __name__ == '__main__':
    hashes1 = []
    hashes2 = []
    links_d1 = get_all_images('/Volumes/tailtq-disk/face_masks/face_mask/images')
    links_d2 = get_all_images('/Volumes/tailtq-disk/face_masks/face_mask2/images')

    for link1 in links_d1:
        pairs = []

        for link2 in links_d2:
            img1 = Image.open(link1)
            img2 = Image.open(link2)

            shape1 = np.array(img1).shape[:2]
            shape2 = np.array(img2).shape[:2]

            if sum(shape1) > sum(shape2):
                img1 = img1.resize(img2.size)
            else:
                img2 = img2.resize(img1.size)

            if nrmse(np.array(img1), np.array(img2)) > 0.95:
                pairs.append([link1, link2])

        print(pairs)
