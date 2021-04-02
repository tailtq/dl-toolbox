import glob
import cv2

from utils.object_recognition_common import predict_bboxes, load_model

root_directory = "/home/tailtq/Downloads/test-set"
ignored_regions = [
    # [3, 0.841818, 0.723077, 0.225455, 0.548718],
    # [3, 0.910606, 0.225000, 0.074545, 0.173077],
]
ignored_regions_coordinates = list(map(lambda ignored_region: [
    ignored_region[1] - ignored_region[3] / 2,  # x1
    ignored_region[2] - ignored_region[4] / 2,  # y1
    ignored_region[1] + ignored_region[3] / 2,  # x2
    ignored_region[2] + ignored_region[4] / 2,  # y2
], ignored_regions))

ignored_regions_str = [" ".join([str(x) for x in xs]) for xs in ignored_regions]

if __name__ == "__main__":
    model = load_model("face-mask-best.pt")

    img_paths = sorted(glob.glob(f"{root_directory}/custom_*.jpg"))
    total_imgs = len(img_paths)
    # img_paths = list(filter(lambda img_path: not os.path.exists(img_path.replace(".jpg", ".txt")), img_paths))

    for index, img_path in enumerate(img_paths):
        print(f"{index + 1}/{total_imgs} {img_path}")

        img_name = img_path.split("/")[-1].split(".")[0]
        img = cv2.imread(img_path)
        result, orig_img, _ = predict_bboxes(img, model, 800)

        text = ""
        height, width, _ = orig_img.shape

        for det in result:
            # check boxes inside ignored regions?
            in_ignored_region = False
            x1, y1, x2, y2 = det[0] / width, \
                             det[1] / height, \
                             det[2] / width, \
                             det[3] / height

            for index, ignored_region in enumerate(ignored_regions_coordinates):
                if ignored_region[0] <= x1 and ignored_region[2] >= x2 and ignored_region[1] <= y1 and ignored_region[3] >= y2:
                    in_ignored_region = True
                    break

            if in_ignored_region:
                continue

            label = [
                str(int(det[5])),
                str((det[0] + det[2]) / 2 / width),
                str((det[1] + det[3]) / 2 / height),
                str(abs(det[0] - det[2]) / width),
                str(abs(det[1] - det[3]) / height),
            ]
            text += " ".join(label) + "\n"

        text += "\n".join(ignored_regions_str)

        # shutil.copy(img_path, "dataset/train2/")
        stream = open(f"{root_directory}/{img_name}.txt", "w+")
        stream.write(text)
        stream.close()
#  python ~/Code/machine-learning/labelImg/labelImg.py /Users/tailtq/Code/machine-learning/cable-detection/original-dataset-should-save /Users/tailtq/Code/machine-learning/cable-detection/original-dataset-should-save/classes.txt /Users/tailtq/Code/machine-learning/cable-detection/original-dataset-should-save
