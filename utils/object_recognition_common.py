import cv2
import imutils
import torch
import numpy as np

from models.experimental import attempt_load
from utils.datasets import letterbox
from utils.general import non_max_suppression, scale_coords
from utils.plots import plot_one_box

device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("cpu")
half = device.type != "cpu"

CATEGORIES = ["head", "head_2", "mask"]
COLORS = [(66, 135, 245), (194, 66, 245), (250, 52, 72)]


def load_model(path):
    model = attempt_load(path, map_location=device)

    if half:
        model.half()

    return model


def convert_img(img, device, half, new_size=416):
    img = letterbox(img, new_shape=new_size)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)

    img = img.half() if half else img.float()
    img = img / 255.0

    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    return img


def predict_bboxes(img, model, resized_width):
    orig_img = img.copy()

    plot_img = orig_img.copy()
    img = convert_img(orig_img, device, half, new_size=resized_width)
    _, _, new_height, new_width = img.size()

    preds = model(img)[0]
    preds = non_max_suppression(preds, 0.4, 0.5)
    result = np.array([], dtype=np.float32)

    # based on YOLOv5
    for i, det in enumerate(preds):  # detections per image
        if det is not None:
            # Rescale boxes from img_size to im0 size
            det[:, :4] = scale_coords(img.size()[2:], det[:, :4], orig_img.shape).round()
            result = det.type(torch.float32).cpu().detach().numpy()

            # for visualization only
            for *xyxy, conf, cls in reversed(det):
                label = '%s %.2f' % (CATEGORIES[int(cls)], conf)
                plot_one_box(xyxy, plot_img, label=label, color=COLORS[int(cls)], line_thickness=3)

    return result, orig_img, plot_img


def get_center(coordinates):
    tl_x, tl_y = coordinates[:2]
    br_x, br_y = coordinates[2:4]

    return round((tl_x + br_x) / 2), round((tl_y + br_y) / 2)


def draw_bbox(coordinates, img, classes):
    for coordinate in coordinates:
        cv2.rectangle(img, tuple(coordinate[0:2].tolist()), tuple(coordinate[2:4].tolist()), (0, 255, 0), 2)
        cv2.putText(img, classes[coordinate[5]], tuple(coordinate[0:2].tolist()), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    return img
