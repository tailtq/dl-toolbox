import cv2
import numpy as np
import unidecode


# return top left, width and height
def get_yolo_img(img_path, classes):
    txt_path = img_path.split('.')[0] + '.txt'

    img = cv2.imread(img_path)
    height, width, _ = img.shape
    annotations = []

    if classes is not None:
        lines = open(txt_path, 'r').readlines()

        for line in lines:
            annotation = line.strip().split(' ')
            category_index, x, y, w, h = annotation
            category_index = int(category_index)
            x = int(float(x) * width)
            y = int(float(y) * height)
            w = int(float(w) * width)
            h = int(float(h) * height)
            x = int(x - w / 2)
            y = int(y - h / 2)
            annotations.append([category_index, x, y, w, h])

    return img, np.array(annotations)


def plot_annotations(img, annotations, classes, color=(0, 0, 255)):
    new_img = img.copy()

    for annotation in annotations:
        plot_annotation(new_img, annotation, classes, color)

    return new_img


def plot_annotation(img, annotation, classes, color=(0, 0, 255)):
    point1 = tuple(annotation[1:3])
    point2 = annotation[1] + annotation[3], annotation[2] + annotation[4]

    cv2.rectangle(img, point1, point2, color, thickness=2)
    cv2.putText(img,
                unidecode.unidecode(classes[annotation[0]]),
                (point1[0], point2[1]),
                0,
                0.4,
                color=color,
                thickness=1)

# def convert_yolo_labels_to_coordinates(annotations):
#     coordinates = []
#     # clockwise
#     for annotation in annotations:
#         p1 = annotation[1] - annotation[3] / 2, annotation[2] - annotation[4] / 2
#         p2 = p1[0] + annotation[3], p1[1]
#         p3 = p1[0] + annotation[3], p1[1] + annotation[4]
#         p4 = p1[0], p1[1] + annotation[4]
#
#         coordinates.append([annotation[0], p1, p2, p3, p4])
#
#     return coordinates
#
#
# def convert_coordinates_to_yolo_labels(coordinates_sets, img_shape, classes):
#     annotations = []
#     height, width, _ = img_shape
#
#     for coordinates in coordinates_sets:
#         coordinate1, coordinate2, coordinate3, coordinate4 = coordinates[1:]
#         annotations.append([
#             str(classes.index(coordinates[0])),
#             str((coordinate1[0] + coordinate2[0]) / 2 / width),
#             str((coordinate1[1] + coordinate3[1]) / 2 / height),
#             str(abs(coordinate1[0] - coordinate2[0]) / width),
#             str(abs(coordinate1[1] - coordinate3[1]) / height),
#         ])
#
#     return annotations


def change_annotations_by_size(annotations, old_shape, new_shape):
    if len(annotations) == 0:
        return annotations

    old_height, old_width = old_shape[:2]
    new_height, new_width = new_shape[:2]

    annotations[:, 1] = annotations[:, 1] * new_width / old_width
    annotations[:, 2] = annotations[:, 2] * new_height / old_height
    annotations[:, 3] = annotations[:, 3] * new_width / old_width
    annotations[:, 4] = annotations[:, 4] * new_height / old_height

    return annotations


def read_classes_file(path):
    return open(path, 'r').read().split('\n')
