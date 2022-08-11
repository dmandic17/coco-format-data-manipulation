import json
from pathlib import Path
import argparse

class CocoExtractor():
    def __init__(self) -> None:
        pass

    def extract_categories(args):
        pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract categories from COCO JSON annotation. ")
    parser.add_argument("-i", "--input_ann", dest="input_ann",
        help="path to a json annotation file in coco format")
    parser.add_argument("-o", "--output_ann", dest="output_ann",
        help="path to save the output json annotation file")
    parser.add_argument("-c", "--categories", nargs='+', dest="categories",
        help="List of category names separated by spaces, e.g. -c \"person\" \"dog\" \"cat\"")

    args = parser.parse_args()

    cf = CocoExtractor()
    cf.extract_categories(args)