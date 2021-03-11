import os
import cv2
import glob
import imutils
import numpy as np

from utils.dataset.yolo_util import get_yolo_img


def split_images_by_equal_parts(segment_num: tuple, directory_path):
    image_links = glob.glob(directory_path + '/*.jpg')
    new_dir = directory_path + '_1'
    width_num, height_num = segment_num

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for link in image_links:
        img = cv2.imread(link)
        img_name = link.split('/')[-1].split('.jpg')[0]
        height, width, _ = img.shape

        start_width = 0
        width_part = int(width / width_num)

        start_height = 0
        height_part = int(height / height_num)

        index = 0

        for i in range(height_num):
            for j in range(width_num):
                part = img[start_height:start_height + height_part, start_width:start_width + width_part]
                part = imutils.resize(part, width=1280)
                cv2.imwrite('{}/{}_{}.jpg'.format(new_dir, img_name, index), part)

                index += 1
                start_width += width_part

            start_width = 0
            start_height += height_part


def split_custom_size(directory_path):
    image_links = sorted(glob.glob(directory_path + '/*.jpg'))
    new_dir = directory_path + '_1'

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    for link in image_links:
        img, annotations = get_yolo_img(link)
        img_name = link.split('/')[-1].split('.jpg')[0]
        # 300 --> 950 || 150 --> 875
        # TODO: Change custom sizes here
        # log
        # new_img = img[150:875, 800:]

        new_img = img
        # new_width = new_img.shape[1]
        # compared to img
        # [300:, 840: 1800]
        # start_pos1 = (150, 800 + int(new_width / 2))
        # start_pos2 = (150, 800)

        # size: 580x785
        # 350x350
        # new_img1 = new_img[215:565, :350]
        # new_img2 = new_img[150:630, 850:]

        # 456:898, 0:620
        new_img1 = new_img[456:898, 0:620]
        new_img2 = new_img[500:, 925:]

        new_img1 = imutils.resize(new_img1, width=1024)
        new_img2 = imutils.resize(new_img2, width=1024)

        # cv2.imshow('Test', new_img1)
        # cv2.imshow('Test2', new_img2)
        # cv2.waitKey(-1)

        cv2.imwrite('{}/{}_1.jpg'.format(new_dir, img_name), new_img1)
        cv2.imwrite('{}/{}_2.jpg'.format(new_dir, img_name), new_img2)

        # old_shape1 = new_img1.shape
        # new_labels1 = []
        # old_shape2 = new_img2.shape
        # new_labels2 = []

        # for annotation in annotations:
        #     label1 = infer_label(annotation, new_img1.shape, start_pos1)
        #     if label1 is not None:
        #         new_labels1.append(label1)
        #
        #     label2 = infer_label(annotation, new_img2.shape, start_pos2)
        #     if label2 is not None:
        #         new_labels2.append(label2)

            # if img_name == '0_frame_0000810':
            #     print(annotation, label1, label2)

        # new_img1 = imutils.resize(new_img1, width=768)
        # new_img2 = imutils.resize(new_img2, width=896)

        # new_shape1 = new_img1.shape
        # new_shape2 = new_img2.shape

        # for index, label1 in enumerate(new_labels1):
        #     new_labels1[index] = rescale_label(label1, old_shape1, new_img1.shape)

        # for index, label2 in enumerate(new_labels2):
        #     new_labels2[index] = rescale_label(label2, old_shape2, new_img2.shape)



        # if len(new_labels1) > 0:
        #     new_labels1 = np.array(new_labels1)
        #     new_labels1[:, 1] = new_labels1[:, 1] / new_shape1[1]
        #     new_labels1[:, 3] = new_labels1[:, 3] / new_shape1[1]
        #     new_labels1[:, 2] = new_labels1[:, 2] / new_shape1[0]
        #     new_labels1[:, 4] = new_labels1[:, 4] / new_shape1[0]
        #     new_labels1 = new_labels1.astype(str)
        #     new_labels1[:, 0] = [str(int(float(x))) for x in new_labels1[:, 0]]
        #
        #     f = open('{}/{}_1.txt'.format(new_dir, img_name), 'w+')
        #     f.write('\n'.join(map(lambda x: ' '.join(x), new_labels1)))
        #     f.close()

        # if len(new_labels2) > 0:
        #     new_labels2 = np.array(new_labels2)
        #     new_labels2[:, 1] = new_labels2[:, 1] / new_shape2[1]
        #     new_labels2[:, 3] = new_labels2[:, 3] / new_shape2[1]
        #     new_labels2[:, 2] = new_labels2[:, 2] / new_shape2[0]
        #     new_labels2[:, 4] = new_labels2[:, 4] / new_shape2[0]
        #     new_labels2 = new_labels2.astype(str)
        #     new_labels2[:, 0] = [str(int(float(x))) for x in new_labels2[:, 0]]
        #
        #     f = open('{}/{}_2.txt'.format(new_dir, img_name), 'w+')
        #     f.write('\n'.join(map(lambda x: ' '.join(x), new_labels2)))
        #     f.close()


# infer old coordinates to new coordinates
def infer_label(annotation, new_shape, new_shape_position):
    replacement_y, replacement_x = new_shape_position
    new_height, new_width, _ = new_shape

    label_new_position = (
        float(annotation[0]),
        float(annotation[1] - replacement_x),
        float(annotation[2] - replacement_y),
        float(annotation[3]),
        float(annotation[4]),
    )

    # check position in new shape:
    # 3 cases:
    # - IGNORE: left < 0 or top < 0:
    # - IGNORE: left + width > img_width or top + height > img_height:
    # - ACCEPT: left >= 0 and top >= 0 and left + width < img_width and top + height < img_height:
    if label_new_position[1] < 0 or \
            label_new_position[2] < 0 or \
            label_new_position[1] > new_width or \
            label_new_position[2] > new_height:
        return None

    return label_new_position


def rescale_label(annotation, old_shape, new_shape):
    ratio_width = float(new_shape[1]) / old_shape[1]
    ratio_height = float(new_shape[0]) / old_shape[0]
    new_x = annotation[1] * ratio_width
    new_y = annotation[2] * ratio_height
    new_width = annotation[3] * ratio_width
    new_height = annotation[4] * ratio_height

    return (
        annotation[0],
        new_x,
        new_y,
        new_width,
        new_height,
    )


if __name__ == '__main__':
    directories = ['data/10-01-02_544052']

    for directory in directories:
        # split_images_by_equal_parts((2, 2), directory)
        split_custom_size(directory)
