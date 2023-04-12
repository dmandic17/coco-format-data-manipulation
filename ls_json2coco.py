import json
import argparse

def main(args):
    f = open(args.in_path)
    in_ann = json.load(f)
    f.close()


    out_ann = {}
    out_ann['licenses'] = [{
                "id": 1,
                "name": "Attribution-NonCommercial-ShareAlike License",
                "url": "http://creativecommons.org/licenses/by-nc-sa/2.0/"
            }]
    out_ann['info'] = {}

    images = []
    annotations = []

    categories = {}
    ann_id = 0
    cat_id = 1

    for in_img in in_ann:
        out_img = {}
        id = in_img['id'] - 1
        out_img['id'] = id
        out_img['file_name'] = in_img['url'].split('-')[1]
        out_img['height'] = in_img['kp-1'][0]['original_height']
        out_img['width'] = in_img['kp-1'][0]['original_width']
        out_img['label_type'] = 'points'
        images.append(out_img)

        for in_ann in in_img['kp-1']:
            ann = {}
            ann['image_id'] = id
            ann['id'] = ann_id
            ann_id += 1
            ann['point'] = [in_ann['x'], in_ann['y']]
            category = in_ann['keypointlabels'][0]
            if category not in categories.keys():
                categories[category] = cat_id
                cat_id += 1
            ann['category_id'] = categories[category]
            annotations.append(ann)

    categories_out = []
    for category in categories.keys():
        cat = {}
        cat['id'] = categories[category]
        cat['name'] = category
        categories_out.append(cat)


    out_ann['images'] = images
    out_ann['annotations'] = annotations
    out_ann['categories'] = categories_out


    f = open(args.out_path, 'w')
    json.dump(out_ann, f)
    f.close()

if __name__ == '__main__':
    argParser = argparse.ArgumentParser()
    required = argParser.add_argument_group('required arguments')
    required.add_argument('-i', '--in_path', help='Path to input annotation file in label studio json format.', required=True)
    argParser.add_argument('-o', '--out_path', action='store_true', help='Path to output annotation file - coco format output.')

    args = argParser.parse_args()
    main(args)

    print("Done.")