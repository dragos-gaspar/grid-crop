import os
import re
import json

import xmltodict
from skimage import io

import config


config.INPUT_PATHS = [os.path.join(config.INPUT_BASE, inp) for inp in config.INPUT_PATHS]


def make_dir(dir_path: str):
    """
    Create a directory if it does not exist

    :param dir_path: absolute path to the directory
    :return: path to the directory if successful or None if and error occurred
    """

    try:
        isdir = os.path.isdir(dir_path)
        if not isdir:
            os.mkdir(dir_path)
        return dir_path

    except Exception as error:
        print(error)
        return None


def get_bbox_from_xml(path: str):
    with open(path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()
    bounding_boxes = data_dict["annotation"]["object"]
    bounding_boxes = [bb["bndbox"] for bb in bounding_boxes]

    return bounding_boxes


def crop_image(image_meta, input_path):
    """
    Crop an image in a grid-like fashion according to sizes defined in config.py
    Save images to disk along with resulting bounding box information as json

    :param image_meta: Tuple that contains (image_name, bounding_box)
    :param input_path: Base input path
    :return: None
    """
    # Load image
    image = io.imread(os.path.join(input_path, image_meta[0]))

    # Load bounding boxes
    bounding_boxes = get_bbox_from_xml(os.path.join(input_path, image_meta[1]))

    # Get size cues
    h, w, c = image.shape
    h_grid, w_grid = int(h // config.CROP_HEIGHT), int(w // config.CROP_WIDTH)

    # Cropping loop
    for i in range(h_grid):
        for j in range(w_grid):
            # Calculate crop coordinates
            crop_offset_x, crop_offset_y = j * config.CROP_WIDTH, i * config.CROP_HEIGHT
            crop_rect = {
                'xmin': crop_offset_x,
                'ymin': crop_offset_y,
                'xmax': crop_offset_x + config.CROP_WIDTH,
                'ymax': crop_offset_y + config.CROP_HEIGHT
            }

            # Actual crop
            crop = image[crop_offset_y: crop_offset_y + config.CROP_HEIGHT,
                         crop_offset_x: crop_offset_x + config.CROP_WIDTH]

            # Compute bounding boxes for current crop;
            # these are the intersections of the current crop and each bounding box
            bb_json = []
            for bb in bounding_boxes:
                # Cast bb coordinates to int
                bb = {k: int(v) for k, v in bb.items()}

                # Calculate intersection sides' lengths
                dx = min(crop_rect['xmax'], bb['xmax']) - max(crop_rect['xmin'], bb['xmin'])
                dy = min(crop_rect['ymax'], bb['ymax']) - max(crop_rect['ymin'], bb['ymin'])

                # Check if intersection actually occurs
                if dx >= 0 and dy >= 0:
                    # Thresholding
                    if dx >= config.THRESHOLD['width'] and dy >= config.THRESHOLD['height'] \
                            and dx*dy >= config.THRESHOLD['area']:
                        box = {
                            'xmin': max(crop_rect['xmin'], bb['xmin']) - crop_offset_x,
                            'ymin': max(crop_rect['ymin'], bb['ymin']) - crop_offset_y,
                            'xmax': min(crop_rect['xmax'], bb['xmax']) - crop_offset_x,
                            'ymax': min(crop_rect['ymax'], bb['ymax']) - crop_offset_y
                        }
                        bb_json.append(box)

            # Construct names
            base_name = f"{os.path.splitext(image_meta[0])[0]}_{(i * w_grid + j):03d}"
            crop_name = f"{base_name}.jpg"
            json_name = f"{base_name}.json"
            print(f"Saving {base_name}...")

            # Save image
            io.imsave(
                os.path.join(
                    make_dir(
                        os.path.join(
                            config.OUTPUT_PATH,
                            os.path.basename(input_path)
                        )
                    ),
                    crop_name
                ),
                crop,
                check_contrast=False
            )

            # Save json
            with open(
                os.path.join(
                    make_dir(
                        os.path.join(
                            config.OUTPUT_PATH,
                            os.path.basename(input_path)
                        )
                    ),
                    json_name
                ),
                'w'
            ) as f:
                json.dump(bb_json, f)


def main():
    # Loop through input dirs list; run for every dir
    for input_path in config.INPUT_PATHS:
        print(f"Loading from {input_path}...")

        # Get list of files to load
        input_contents = [f for f in os.listdir(input_path)
                          if re.search(r"\.xml$|\.jpg$|\.jpeg$|\.png$", f) is not None]

        # Separate xml from images
        xml_files, image_files = [], []

        for f in input_contents:
            if f.endswith('.xml'):
                xml_files.append(f)
            else:
                image_files.append(f)

        # Sanity check
        assert len(xml_files) == len(image_files), \
            f"Number of .xml files and number of images don't match in {input_path}"

        # Sort files (for cross platform compatibility)
        xml_files.sort()
        image_files.sort()

        # Process images
        for image_meta in zip(image_files, xml_files):
            crop_image(image_meta, input_path)

    print("Success! 😃")


if __name__ == '__main__':
    main()
