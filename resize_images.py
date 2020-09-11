import os
import cv2
import glob
import imutils
import numpy as np
from PIL import Image
import shutil

quality = 95
saved_directory = 'resized_data'
image_links = glob.glob('dataset/*.JPG')
# label_links = glob.glob('Cable_train.v1-cable_train_flip.yolov5pytorch/train/labels/*.jpg')

os.makedirs(saved_directory, exist_ok=True)

for link in image_links:
    new_link = saved_directory + '/' + link.split('/')[-1]

    # image = cv2.imread(link)
    image = Image.open(link)

    # resize
    image = np.array(image)
    image = imutils.resize(image, width=1920)

    image = Image.fromarray(image)
    image.save(new_link, quality=quality)

    print(new_link)
