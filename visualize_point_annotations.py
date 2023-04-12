import json
import os
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import mmcv
from pycocotools.coco import COCO
import cv2
import argparse


argParser = argparse.ArgumentParser()
required = argParser.add_argument_group('required arguments')
required.add_argument("-i", "--img_path", help="Path to a folder containing the images.", required=True)
required.add_argument("-a", "--ann_path", help="Annotation file with weak annotations.", required=True)
argParser.add_argument("-n", "--num_images", type=int, default=3, help="Number of images to show.")

args = argParser.parse_args()

img_prefix= args.img_path
path = args.ann_path
file = open(path)
coco_api = COCO(path)
ann = json.load(file)
out_dir = 'out_visualize_points'

os.mkdir(out_dir)
    
EPS = 1e-2

images = ann['images']
annotations = ann['annotations']
print('started')
for image in images:
    image_id = image['id']
    if image_id >= args.num_images:
        break
    
    if image['label_type'] == 'points':
        print('here')
        img = mmcv.imread(os.path.join(img_prefix, image['file_name'])).astype(np.uint8)
        img = mmcv.bgr2rgb(img)
        width, height = img.shape[1], img.shape[0]
        img = np.ascontiguousarray(img)
        fig = plt.figure(image['file_name'], frameon=False)
        canvas = fig.canvas
        dpi = fig.get_dpi()
        fig.set_size_inches((width + EPS) / dpi, (height + EPS) / dpi)
        plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
        plt.imshow(img)
        ax = plt.gca()
        ax.axis('off')

        for annotation in annotations:
            # print(image_id)
            if annotation['image_id'] == image_id:
              ax.scatter(annotation['point'][0],annotation['point'][1], c='blue', s=60)

        
        stream, _ = canvas.print_to_buffer()
        buffer = np.frombuffer(stream, dtype='uint8')
        img_rgba = buffer.reshape(height, width, 4)
        rgb, alpha = np.split(img_rgba, [3], axis=2)
        img = rgb.astype('uint8')
        img = mmcv.rgb2bgr(img)


        out_path = os.path.join(out_dir, image['file_name'])
        print(out_path)
        # mmcv.imwrite(img, out_path)
        cv2.imwrite(out_path, img)
        plt.savefig(out_path, bbox_inches='tight')
        plt.close()
        