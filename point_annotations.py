import json
import numpy as np
import random
import os
import cv2
from pycocotools.coco import COCO
import sys
import argparse

def main(args):

    out_root_dir = './'
    ann_path = args.ann_path
    json_file = os.path.join(ann_path)
    coco_api = COCO(json_file)
    random_seed = 1709

    # Change this depending on the requirements:
    img_ids = sorted(coco_api.imgs.keys())
    random.seed(random_seed)
    imgs_all = []
    anns_all = []

    imgs = coco_api.loadImgs(img_ids)

    for i_img in imgs:
        i_img['label_type'] = 'points'

    dataset_anns_u = [coco_api.imgToAnns[img_id] for img_id in img_ids]
    anns = [ann for img_anns in dataset_anns_u for ann in img_anns]

    # os.mkdir('masks')
    ith = 0
    for i_ann in anns:

        boxes = i_ann['bbox']
        boxes = np.array(boxes)
        h, w = int(boxes[3]),int(boxes[2])
        x, y = int(boxes[0]), int(boxes[1])

        if args.center:
            i_ann['point'] = [float(x + w//2), float(y + h//2)]
            continue
        else:
            mask_i = coco_api.annToMask(i_ann)
            size = int(np.sqrt(np.sum(mask_i)//8))
            kernel = np.ones((size, size), np.uint8)
            mask_i = cv2.erode(mask_i, kernel, cv2.BORDER_REFLECT)
            valid_idx = np.where(mask_i == 1)
            
            if np.sum(valid_idx) > 0:
                if args.bottom:
                    sampled_idx = max(valid_idx[0])
                    sampled_point_i = [x+w//2, sampled_idx]
                    sampled_point_i = [float(item) for item in sampled_point_i]
                    i_ann['point'] = sampled_point_i
                else:
                    sampled_idx = np.random.choice(np.arange(np.size(valid_idx[0])), 1)
                    sampled_point_i = [valid_idx[1][sampled_idx][0], valid_idx[0][sampled_idx][0]]
                    sampled_point_i = [float(item) for item in sampled_point_i]
                    i_ann['point'] = sampled_point_i
            else:
                x_min = x + w//4
                x_max = x + w - w//4
                y_min = y + h//4
                y_max = y + h - h//4
                i_ann['point'] = [random.randint(x_min, x_max), random.randint(y_min, y_max)]

    
            i_ann.pop('segmentation')
            i_ann.pop('bbox')
            i_ann.pop('area')
            ith = ith + 1
            if ith % 10000 == 0:
                print(ith)

    imgs_all.extend(imgs)
    anns_all.extend(anns)

    # change idx:
    img_idx = 0
    ann_idx = 0
    for img in imgs_all:
        for ann in anns_all:
            if ann['image_id'] == img['id']:
                ann['image_id'] = img_idx
                ann['id'] = ann_idx
                ann_idx += 1
        img['id'] = img_idx 
        img_idx += 1

    data = {}
    data['images'] = imgs_all
    data['annotations'] = anns_all
    data['categories'] = list(coco_api.cats.values())
    data['info'] = coco_api.dataset['info']
    data['licenses'] = coco_api.dataset['licenses']

    filename = os.path.basename(ann_path)
    filename = filename[:-5]

    output_file = os.path.join(out_root_dir, 'points_' + filename+ '.json' )
    if args.center:
        output_file = os.path.join(out_root_dir, 'ct_points_' + filename+ '.json' )
    if args.bottom:
        output_file = os.path.join(out_root_dir, 'bt_points_' + filename+ '.json' )
    ## save to json
    with open(output_file, 'w') as f:
        print('writing to json output:', output_file)
        json.dump(data, f, sort_keys=True)


if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    required = argParser.add_argument_group('required arguments')
    required.add_argument('-a', '--ann_path', help='Annotation file with bbox annotations.', required=True)
    argParser.add_argument('-c', '--center', action='store_true', help='Sample central points of bboxes.')
    argParser.add_argument('-b', '--bottom', action='store_true', help='Sample bottom point from eroded mask')

    args = argParser.parse_args()
    main(args)

    print("Done.")