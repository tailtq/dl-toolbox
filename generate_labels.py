import glob
import cv2

from utils.object_recognition_common import predict_bboxes, load_model


root_directory = "dataset/real-cases"

if __name__ == "__main__":
    model = load_model("face-mask-best.pt")

    img_paths = sorted(glob.glob(f"{root_directory}/*.jpg"))
    # img_paths = list(filter(lambda img_path: not os.path.exists(img_path.replace(".jpg", ".txt")), img_paths))
    i = 0
    total_imgs = len(img_paths)

    for img_path in img_paths:
        i += 1
        print(f"{i}/{total_imgs} {img_path}")

        img_name = img_path.split("/")[-1].split(".")[0]

        img = cv2.imread(img_path)
        result, orig_img, _ = predict_bboxes(img, model, 800)

        text = ""
        height, width, _ = orig_img.shape

        for det in result:
            label = [
                str(int(det[5])),
                str((det[0] + det[2]) / 2 / width),
                str((det[1] + det[3]) / 2 / height),
                str(abs(det[0] - det[2]) / width),
                str(abs(det[1] - det[3]) / height),
            ]
            text += " ".join(label) + "\n"

        # shutil.copy(img_path, "dataset/train2/")
        stream = open(f"{root_directory}/{img_name}.txt", "w+")
        stream.write(text)
        stream.close()
