# Code adapted from: https://github.com/immersive-limit/coco-manager
# Original code under MIT Licence
# Adapted by: Dejana Mandic @dmandic17
# Changes made: 
#   - Code reformated
#   - Arguments requirements minor changes (to account for categories containing space character)
#   - Progress tracking added
#   - Testing added in coco_categories.py
#   - Class listing can also be found int coco_categories.py
#   - Exception handling added for unknown paths

import json
from pathlib import Path
import argparse

class CocoExtractor():
    def __init__(self) -> None:
        pass
    
    # Reading categories, and corresponding supercategories from coco format:
    def read_categories(self):
        self.categories = dict()
        self.super_categories = dict()
        self.category_set = set()

        for category in self.coco['categories']:
            cat_id = category['id']
            try:
                super_category = category['supercategory']
            except KeyError:
                super_category = 'all'
            
            # Add category to categories dict
            if cat_id not in self.categories:
                self.categories[cat_id] = category
                self.category_set.add(category['name'])
            else:
                print(f'ERROR: Skipping duplicate category id: {category}')
            
            # Add category id to the super_categories dict
            if super_category not in self.super_categories:
                self.super_categories[super_category] = {cat_id}
            else:
                self.super_categories[super_category] |= {cat_id} # e.g. {1, 2, 3} |= {4} => {1, 2, 3, 4}

    # Reading the images:
    def read_images(self):
        self.images = dict()
        for image in self.coco['images']:
            image_id = image['id']
            if image_id not in self.images:
                self.images[image_id] = image
            else:
                print(f'ERROR: Skipping duplicate image id: {image}')

    # Reading segmentations/bboxes:        
    def read_segmentations(self):
        self.segmentations = dict()
        for segmentation in self.coco['annotations']:
            image_id = segmentation['image_id']
            if image_id not in self.segmentations:
                self.segmentations[image_id] = []
            self.segmentations[image_id].append(segmentation)

    # Filter by categories
    def filtering_categories(self):
        """ Find category ids matching args
            Create mapping from original category id to new category id
            Create new collection of categories
        """
        missing_categories = set(self.filter_categories) - self.category_set
        if len(missing_categories) > 0:
            print(f'Did not find categories: {missing_categories}')
            should_continue = input('Continue? (y/n) ').lower()
            if should_continue != 'y' and should_continue != 'yes':
                print('Quitting early.')
                quit()

        self.new_category_map = dict()
        new_id = 1
        for key, item in self.categories.items():
            if item['name'] in self.filter_categories:
                self.new_category_map[key] = new_id
                new_id += 1

        self.new_categories = []
        for original_cat_id, new_id in self.new_category_map.items():
            new_category = dict(self.categories[original_cat_id])
            new_category['id'] = new_id
            self.new_categories.append(new_category)

    def filtering_annotations(self):
        """ Create new collection of annotations matching category ids
            Keep track of image ids matching annotations
        """
        self.new_segmentations = []
        self.new_image_ids = set()
        for image_id, segmentation_list in self.segmentations.items():
            for segmentation in segmentation_list:
                original_seg_cat = segmentation['category_id']
                if original_seg_cat in self.new_category_map.keys():
                    new_segmentation = dict(segmentation)
                    new_segmentation['category_id'] = self.new_category_map[original_seg_cat]
                    self.new_segmentations.append(new_segmentation)
                    self.new_image_ids.add(image_id)

    def filtering_images(self):
        """ Create new collection of images
        """
        self.new_images = []
        for image_id in self.new_image_ids:
            self.new_images.append(self.images[image_id])


    def extract_categories(self,args):

        # Load the arguments
        print('Reading arguments...')

        self.input_ann_path = Path(args.input_ann)
        print("Input path:", self.input_ann_path)

        self.output_ann_path = Path(args.output_ann)
        print("Output path:", self.output_ann_path)

        self.filter_categories = args.categories
        print("Categories for filtering:", self.filter_categories)

        # Load the annotation file if it exists
        print('Opening input annotations file...')
        try:
            with open(self.input_ann_path) as json_file:
                self.coco = json.load(json_file)
        except EnvironmentError:
            print("ERROR: Couldn't read input annotation file.")
            quit()

        # Reading info and licences:
        print('Reading info and licenses...')
        self.info = self.coco['info']
        self.licenses = self.coco['licenses']
        
        # Process the annnotations
        print('Reading categories...')
        self.read_categories()
        print('Reading images...')
        self.read_images()
        print('Reading segmentations...')
        self.read_segmentations()

        # Filter to specific categories
        print('Filtering categories...')
        self.filtering_categories()
        print('Filtering annotations...')
        self.filtering_annotations()
        print('Filtering images...')
        self.filtering_images()

        # Build new annotation
        print('Making new annotations file...')
        new_ann = {
            'info': self.info,
            'licenses': self.licenses,
            'images': self.new_images,
            'annotations': self.new_segmentations,
            'categories': self.new_categories
        }

        # Write the JSON to a file
        print('Saving new annotation file...')
        try:
            with open(self.output_ann_path, 'w+') as output_file:
                json.dump(new_ann, output_file)
        except EnvironmentError:
            print("ERROR: Couldn't write to the output file, please check your permissions and the path correctness.")
            quit()

        print('Filtered json saved.')


if __name__ == "__main__":
    print('Parsing the arguments...')
    parser = argparse.ArgumentParser(description="Extract subset of categories from COCO JSON annotation. ")
    parser.add_argument("-i", "--input_ann", dest="input_ann",
        help="path to a json annotation file in coco format")
    parser.add_argument("-o", "--output_ann", dest="output_ann",
        help="path to save the output json annotation file")
    parser.add_argument("-c", "--categories", nargs='+', dest="categories",
        help="List of category names separated by spaces, e.g. -c \"person\" \"dog\" \"cat\"")

    args = parser.parse_args()

    cf = CocoExtractor()
    cf.extract_categories(args)