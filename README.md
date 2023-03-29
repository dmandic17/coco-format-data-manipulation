# Coco format category extraction for object detection

### Functionality:
- The script ```coco_extraction.py``` allows you to create new annotation file in Coco format from an existing one using the chosen subset of categories.
- The script ```coco_categories.py``` allows you to list all categories from a given annotation file, or to compare the list of categories given with the ones in the annotation file (was used to test the extraction - but can also be used to check for errors).

### Usage:
#### Category subset extraction: 
```
python3 coco_extraction.py [-h] [-i INPUT_ANN] [-o OUTPUT_ANN] [-c CATEGORIES [CATEGORIES ...]]
```

```
Optional arguments:
  -h, --help            show this help message and exit
  -i INPUT_ANN, --input_ann INPUT_ANN
                        path to a json annotation file in coco format
  -o OUTPUT_ANN, --output_ann OUTPUT_ANN
                        path to save the output json annotation file
  -c CATEGORIES [CATEGORIES ...], --categories CATEGORIES [CATEGORIES ...]
                        List of category names separated by spaces, e.g. -c
                        "person" "dog" "cat"

```
#### Category listing and comparing:
```
python3 coco_categories.py [-h] [-i ANN] [-c CATEGORIES [CATEGORIES ...]] [-l]
```
```

Optional arguments:
  -h, --help            show this help message and exit
  -i ANN, --ann ANN     Path to a json annotation file in coco format
  -c CATEGORIES [CATEGORIES ...], --categories CATEGORIES [CATEGORIES ...]
                        List of category names separated by spaces, e.g. -c
                        "person" "dog" "cat"
  -l, --list            Print all the categories found in the input annotation
                        file.

```
