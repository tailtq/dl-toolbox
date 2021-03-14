import cv2
import glob
import os
from natsort import natsorted, ns

# import imutils
#
#
# files = glob.glob("dataset/real-cases/273271,*.jpg")
#
# for file in files:
#     img = cv2.imread(file)
#     img = imutils.resize(img, width=400)
#     cv2.imwrite(file, img)

files = sorted(glob.glob("dataset/obj_train_data/273271,*.jpg"))

for file in files[101:]:
    os.remove(file)
