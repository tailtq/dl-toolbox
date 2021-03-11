import cv2
import glob
import imutils


files = glob.glob("dataset/head_data/*.jpg")

for file in files:
    img = cv2.imread(file)
    img = imutils.resize(img, width=400)
    cv2.imwrite(file, img)
