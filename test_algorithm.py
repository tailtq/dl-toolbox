import cv2
import torch
import numpy as np

from add_ignored_areas import read_n_parse_label
from utils.general import box_iou

img_path = "/home/tailtq/Code/AI/dl-toolbox/visualization/data/maksssksksss674.png"
txt_path = "/home/tailtq/Code/AI/dl-toolbox/visualization/data/maksssksksss674.txt"
img = cv2.imread(img_path)
img_copy = img.copy()

labels, _ = read_n_parse_label(txt_path, img.shape)
ignored_labels = list(filter(lambda label: label[0] == 3, labels))
not_ignored_labels = list(filter(lambda label: label[0] in [0, 1, 2], labels))

for ignored_label in ignored_labels:
    box1 = torch.flatten(torch.tensor(ignored_label[1:5])).view((1, 4))
    overlapped_labels = []

    ignored_x1 = ignored_label[1][0]
    ignored_x2 = ignored_label[2][0]
    ignored_y1 = ignored_label[1][1]
    ignored_y2 = ignored_label[2][1]

    img[ignored_y1:ignored_y2, ignored_x1:ignored_x2] = 255

    for not_ignored_label in not_ignored_labels:
        box2 = torch.flatten(torch.tensor(not_ignored_label[1:5])).view((1, 4))
        iou = box_iou(box1, box2)

        not_ignored_x1 = not_ignored_label[1][0]
        not_ignored_x2 = not_ignored_label[2][0]
        not_ignored_y1 = not_ignored_label[1][1]
        not_ignored_y2 = not_ignored_label[2][1]

        if iou > 0:
            test1 = np.max([[not_ignored_x1, not_ignored_y1], [ignored_x1, ignored_y1]], axis=0)
            test2 = np.min([[not_ignored_x2, not_ignored_y2], [ignored_x2, ignored_y2]], axis=0)
            img[test1[1]:test2[1], test1[0]:test2[0]] = img_copy[test1[1]:test2[1], test1[0]:test2[0]]

cv2.imshow("Test", img)
cv2.waitKey(-1)
