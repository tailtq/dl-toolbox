import os
import urllib.request

import cv2
import imutils
from pycocotools.coco import COCO

from utils.dataset.yolo_util import get_yolo_img, change_annotations_by_size, plot_annotations


def save_img(url, local_url):
    # {
    #     'license': 3,
    #     'file_name': '000000532481.jpg',
    #     'coco_url': 'http://images.cocodataset.org/val2017/000000532481.jpg',
    #     'height': 426,
    #     'width': 640,
    #     'date_captured': '2013-11-20 16:28:24',
    #     'flickr_url': 'http://farm7.staticflickr.com/6048/5915494136_da3cfa7c5a_z.jpg',
    #     'id': 532481
    # }
    try:
        urllib.request.urlretrieve(url, local_url)

        return True
    except:
        return False


def save_anns(anns, txt_path, catIds, img_shape):
    # {
    #     'segmentation': [],
    #     'area': 453.39979999999986,
    #     'iscrowd': 0,
    #     'image_id': 15335,
    #     'bbox': [362.44, 102.44, 24.23, 27.7],
    #     'category_id': 1,
    #     'id': 2025828
    # }
    img_height, img_width = img_shape[:2]
    new_anns = []

    for ann in anns:
        if ann['iscrowd'] == 1:
            continue

        tl_w = ann['bbox'][0]
        tl_h = ann['bbox'][1]
        width = ann['bbox'][2]
        height = ann['bbox'][3]

        # print(ann['bbox'])

        new_anns.append(' '.join([
            str(catIds.index(ann['category_id'])),
            str((tl_w + width / 2) / img_width),
            str((tl_h + height / 2) / img_height),
            str(width / img_width),
            str(height / img_height),
        ]))

    f = open(txt_path, 'w+')
    f.write('\n'.join(new_anns))
    f.close()


def find_anns(annInfo, imgId, catIds):
    # {
    #     'segmentation': [],
    #     'area': 453.39979999999986,
    #     'iscrowd': 0,
    #     'image_id': 15335,
    #     'bbox': [362.44, 102.44, 24.23, 27.7],
    #     'category_id': 1,
    #     'id': 2025828
    # }
    return [ann for ann in annInfo if ann['image_id'] == imgId and ann['category_id'] in catIds]


annotations_path = 'coco/annotations'
train_annotation_path = '{}/instances_train2017.json'.format(annotations_path)
val_annotation_path = '{}/instances_val2017.json'.format(annotations_path)

if __name__ == '__main__':
    # Change here
    save_dir = 'coco/vehicles/train'

    # follow the order of coco dataset
    cats = ['bicycle', 'car', 'motorcycle', 'bus', 'truck']
    # cats = ['person']

    coco = COCO(train_annotation_path)
    # End change

    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    catIds = coco.getCatIds(catNms=cats)
    mainImgIds = []

    for catId in catIds:
        # multiple classes --> list multiple imgIds --> combine --> unique
        imgIds = coco.getImgIds(catIds=[catId])
        mainImgIds.extend(imgIds)

    mainImgIds = list(set(mainImgIds))
    annIds = coco.getAnnIds(imgIds=mainImgIds)

    annInfo = coco.loadAnns(annIds)
    imgInfo = coco.loadImgs(mainImgIds)

    for img in imgInfo:
        img_path = '{}/{}'.format(save_dir, img['file_name'])
        txt_path = '.'.join('{}/{}'.format(save_dir, img['file_name']).split('.')[:-1]) + '.txt'

        anns = find_anns(annInfo, img['id'], catIds)

        if len(anns):
            print('[URL] ', img['flickr_url'], img['coco_url'])

            can_save = save_img(img['coco_url'], img_path)

            if can_save:
                img_shape = cv2.imread(img_path).shape
                save_anns(anns, txt_path, catIds, img_shape)

                # visualize
                # img, annotations = get_yolo_img(img_path, cats)
                # new_img = imutils.resize(img, width=800)
                # annotations = change_annotations_by_size(annotations, img.shape, new_img.shape)
                # new_img = plot_annotations(new_img, annotations, cats)
                #
                # cv2.imshow('Window', new_img)
                # key = cv2.waitKey(-1)
                #
                # if key == ord('q'):
                #     break
