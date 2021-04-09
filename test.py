import glob
import cv2
import imutils

files = sorted(glob.glob("/home/william/Downloads/face-mask-416/*.jpg") + \
               glob.glob("/home/william/Downloads/face-mask-416/*.jpeg") + \
               glob.glob("/home/william/Downloads/face-mask-416/*.png"))
# files = sorted(glob.glob("/home/william/Downloads/face-mask-416/14610.jpg"))

total_files = len(files)

for index, file in enumerate(files):
    print(f"({index + 1}/{total_files}) File name: {file}")
    txt_file = file.replace(".jpg", ".txt").replace(".jpeg", ".txt").replace(".png", ".txt")

    img = cv2.imread(file)
    height, width, _ = imutils.resize(img, width=416).shape
    lines = open(txt_file, "r").readlines()
    new_lines = []

    for index, line in enumerate(lines):
        if line[0] == "1":
            segments = line.split(" ")
            coordinates = [float(segment) for segment in segments[1:5]]
            box_width, box_height = int(width * coordinates[2]), int(height * coordinates[3])

            if box_width <= 9 and box_height <= 9:
                print("Continueeee")
                continue

        new_lines.append(line)

    print(len(new_lines), len(lines))
    f = open(txt_file, "w+")
    f.write("".join(new_lines))
    f.close()
