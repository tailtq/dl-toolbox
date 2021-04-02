from add_ignored_areas import draw_bounding_box
from compare_two_directories import get_all_images, get_file_name_by_img
from utils.general import box_iou
from utils.object_recognition_common import predict_bboxes, load_model, parse_yolo_format
import cv2
import torch
import imutils


files = get_all_images("dataset/val")
model = load_model("face-mask-best.pt")
classes = ["head", "head_2", "mask"]

for file in files:
    img = cv2.imread(file)
    txt_file = get_file_name_by_img(file)

    bboxes, orig_img, _ = predict_bboxes(img, model, 416)
    gt_bboxes = parse_yolo_format(txt_file, orig_img.shape)

    # render failed cases (prediction failed or gt_bbox doesn't have prediction

    for gt_bbox in gt_bboxes:
        gt_bbox.append(["none", None])
        has_prediction = False
        gt_coordinates = torch.tensor([gt_bbox[1:5]])

        for bbox in bboxes:
            coordinates = torch.tensor([bbox[0:4]])
            iou = box_iou(coordinates, gt_coordinates)

            if iou > 0.8:
                gt_bbox[5][0] = "ok" if bbox[5] == float(gt_bbox[0]) else "wrong_class"
                gt_bbox[5][1] = bbox[5]
                break

    for gt_bbox in gt_bboxes:
        if gt_bbox[5] != "ok" and gt_bbox[0] in ("0", "1", "2"):
            # cv2.putText(orig_img, classes[], (gt_bbox[1], gt_bbox[2]))
            draw_bounding_box(orig_img, (gt_bbox[1], gt_bbox[2]), (gt_bbox[3], gt_bbox[4]))

    orig_img = imutils.resize(orig_img, width=640)
    cv2.imshow("test", orig_img)
    key = cv2.waitKey(-1)

    if key == ord("q"):
        break

# visualize failed cases
# run prediction --> loop through labels --> calculate

