import json
from pathlib import Path
import argparse

class CocoExtractorTest():
    def __init__(self) -> None:
        pass
    
    # Reading categories, and corresponding supercategories from coco format:
    def read_categories(self):
        self.categories = dict()
        self.super_categories = dict()
        self.category_set = set()

        for category in self.coco['categories']:
            cat_id = category['id']
            super_category = category['supercategory']
            
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


    def test_categories(self,args):

        # Load the arguments
        print('Reading arguments...')

        self.ann = Path(args.ann)
        print("Annotation path:", self.ann)

        self.categories_wanted = args.categories
        print("Categories wanted:", self.categories_wanted)

        # Load the annotation file if it exists
        print('Opening input annotations file...')
        try:
            with open(self.ann) as json_file:
                self.coco = json.load(json_file)
        except EnvironmentError:
            print("ERROR: Couldn't read the annotation file.")
            quit()
        
        # Process the annnotations
        print('Reading categories...')
        self.read_categories()

        print('Comparing categories...')
        categories_wanted = set(self.categories_wanted)

        if categories_wanted.issubset(self.category_set) and self.category_set.issubset(categories_wanted):
            print('Categories DO match.')
        else:
            print('Categories DO NOT match.')

        print(self.category_set)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract categories from COCO JSON annotation. ")
    parser.add_argument("-i", "--ann", dest="ann",
        help="path to a json annotation file in coco format")
    parser.add_argument("-c", "--categories", nargs='+', dest="categories",
        help="List of category names separated by spaces, e.g. -c \"person\" \"dog\" \"cat\"")

    args = parser.parse_args()

    cf = CocoExtractorTest()
    cf.test_categories(args)