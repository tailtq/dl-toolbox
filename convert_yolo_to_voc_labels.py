import glob
from PIL import Image
from xml.dom import minidom
import xml.etree.cElementTree as ET

CLASS_MAPPING = {
    '0': 'cable',
    '1': 'electric post',
    '2': 'circle cable'
}


def create_root(file_prefix, width, height):
    root = ET.Element('annotations')
    ET.SubElement(root, 'filename').text = '{}.jpg'.format(file_prefix)
    ET.SubElement(root, 'folder').text = 'images'
    size = ET.SubElement(root, 'size')
    ET.SubElement(size, 'width').text = str(width)
    ET.SubElement(size, 'height').text = str(height)
    ET.SubElement(size, 'depth').text = '3'
    return root


def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, 'object')
        ET.SubElement(obj, 'name').text = voc_label[0]
        ET.SubElement(obj, 'pose').text = 'Unspecified'
        ET.SubElement(obj, 'truncated').text = str(0)
        ET.SubElement(obj, 'difficult').text = str(0)
        bbox = ET.SubElement(obj, 'bndbox')
        ET.SubElement(bbox, 'xmin').text = str(int(voc_label[1]))
        ET.SubElement(bbox, 'ymin').text = str(int(voc_label[2]))
        ET.SubElement(bbox, 'xmax').text = str(int(voc_label[3]))
        ET.SubElement(bbox, 'ymax').text = str(int(voc_label[4]))
    return root


def create_file(file_prefix, width, height, voc_labels):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent='   ')

    f = open('{}.xml'.format(file_prefix), 'w+')
    f.write(xmlstr)
    f.close()


def read_file(file_path):
    file_prefix = file_path.split('.txt')[0]
    img = Image.open('{}.jpg'.format(file_prefix))

    w, h = img.size
    with open(file_path, 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            voc.append(CLASS_MAPPING.get(data[0]))
            bbox_width = float(data[3]) * w
            bbox_height = float(data[4]) * h
            center_x = float(data[1]) * w
            center_y = float(data[2]) * h
            voc.append(center_x - (bbox_width / 2))
            voc.append(center_y - (bbox_height / 2))
            voc.append(center_x + (bbox_width / 2))
            voc.append(center_y + (bbox_height / 2))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels)
    print('Processing complete for file: {}'.format(file_path))


def start(dir_name):
    for file in glob.glob(dir_name + '/*.txt'):
        if file.endswith('txt') and file.find('classes') == -1:
            read_file(file)
        else:
            print('Skipping file: {}'.format(file))


if __name__ == '__main__':
    start('data/dataset/training_set')
    start('data/dataset/val_set')
