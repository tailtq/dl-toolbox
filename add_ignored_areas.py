import cv2
import glob


files = sorted(glob.glob("dataset/obj_train_data/*.jpg"))

IGNORED_CLASS_INDEX = 3


def add_white_spot(img, tl: list, br: list):
    img[tl[1]:br[1], tl[0]:br[0]] = 255
    return img


def draw_bounding_box(img, tl: list, br: list):
    print(tl, br)
    cv2.rectangle(img, tl, br, (0, 0, 255), 2)


def read_n_parse_label(link, img_shape):
    height, width = img_shape[:2]
    lines = open(link, "r").readlines()
    bboxes = []

    for i, line in enumerate(lines):
        line = [float(e) for e in line.split(" ")]
        line[0] = int(line[0])

        tl = line[1] - line[3] / 2, line[2] - line[4] / 2
        br = tl[0] + line[3], tl[1] + line[4]
        tl = int(tl[0] * width), int(tl[1] * height)
        br = int(br[0] * width), int(br[1] * height)

        bboxes.append([line[0], tl, br])
        lines[i] = line

    return bboxes, lines


for file_path in files:
    print(file_path)

    text_path = file_path.replace(".jpg", ".txt")
    text_path = text_path.replace(".png", ".txt")

    img = cv2.imread(file_path)
    bboxes, lines = read_n_parse_label(text_path, img.shape)

    for box in bboxes:
        if box[0] == IGNORED_CLASS_INDEX:
            img = add_white_spot(img, box[1], box[2])

    removed_indices = []

    for i, line in enumerate(lines):
        if line[0] == IGNORED_CLASS_INDEX:
            removed_indices.append(i)

        lines[i] = " ".join([str(e) for e in line])

    for i in sorted(removed_indices, reverse=True):
        del lines[i]

    cv2.imwrite(file_path, img)

    f = open(text_path, "w+")
    f.write("\n".join(lines))
    f.close()
