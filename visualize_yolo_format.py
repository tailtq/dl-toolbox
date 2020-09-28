import glob
import cv2
import imutils

from utils.dataset.yolo_util import get_yolo_img, read_classes_file, change_annotations_by_size, plot_annotations

files = sorted(glob.glob('data/dataset/training_set/*.jpg'))
classes = read_classes_file('data/classes.txt')

for file in files:
    img, annotations = get_yolo_img(file, classes)
    new_img = imutils.resize(img, width=1200)
    annotations = change_annotations_by_size(annotations, img.shape, new_img.shape)

    new_img = plot_annotations(new_img, annotations, classes)

    cv2.imshow('Window', new_img)
    key = cv2.waitKey(-1)

    if key == ord('q'):
        break

cv2.destroyAllWindows()
