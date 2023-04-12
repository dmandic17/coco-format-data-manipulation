# Coco format data manipulation

### Functionality:
- The script ```coco_extraction.py``` allows you to create new annotation file in Coco format from an existing one using the chosen subset of categories.
- The script ```coco_categories.py``` allows you to list all categories from a given annotation file, or to compare the list of categories given with the ones in the annotation file (was used to test the extraction - but can also be used to check for errors).
- The script ```point_annotations.py``` allows you to change annotation type from bounding boxes and masks to sampled points (one point per object): the sampled point can be (1) central point; (2) randomly sampled point from the eroded mask; or (3) bottom point of the eroded mask;
- The script ```visualize_point_annotations.py``` allows you to visualize results from point sampling script.
- The script ```ls_json2coco.py``` allows you to convert label studio json format to coco format (for point annotations - no bbox and masks here but can be added).

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
#### Point sampling:
```
python3 point_annotations.py [-h] -a ANN_PATH [-c] [-b]
```
```
Optional arguments:
  -h, --help            show this help message and exit
  -c, --center          Sample central points of bboxes.
  -b, --bottom          Sample bottom point from eroded mask

Required arguments:
  -a ANN_PATH, --ann_path ANN_PATH
                        Annotation file with bbox annotations.
```

#### Visualizing point sampling:
```
python3 visualize_point_annotations.py [-h] -i IMG_PATH -a ANN_PATH [-n NUM_IMAGES]
```
```
Optional arguments:
  -h, --help            show this help message and exit
  -n NUM_IMAGES, --num_images NUM_IMAGES
                        Number of images to show.

Required arguments:
  -i IMG_PATH, --img_path IMG_PATH
                        Path to a folder containing the images.
  -a ANN_PATH, --ann_path ANN_PATH
                        Annotation file with weak annotations.
```
#### Label studio to coco format:
```
python3 ls_json2coco.py [-h] -i IN_PATH [-o]
```
```
Optional arguments:
  -h, --help            show this help message and exit

Required arguments:
  -i IN_PATH, --in_path IN_PATH
                        Path to input annotation file in label studio json
                        format.
  -o, --out_path        Path to output annotation file - coco format output.
```
