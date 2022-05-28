import os
import json

from skimage import io

import config
from utils import make_dir, get_bbox_from_xml


def crop_image(image_meta, input_path) -> None:
    """
    Crop an image in a grid-like fashion according to sizes defined in config.py
    Save images to disk along with resulting bounding box information

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
            for box in bounding_boxes:
                # Cast bb coordinates to int
                bb = box['bndbox']
                bb = {k: int(v) for k, v in bb.items()}

                # Calculate intersection sides' lengths
                dx = min(crop_rect['xmax'], bb['xmax']) - max(crop_rect['xmin'], bb['xmin'])
                dy = min(crop_rect['ymax'], bb['ymax']) - max(crop_rect['ymin'], bb['ymin'])

                # Check if intersection actually occurs
                if dx >= 0 and dy >= 0:
                    # Thresholding
                    if dx >= config.THRESHOLD['width'] and dy >= config.THRESHOLD['height'] \
                            and dx*dy >= config.THRESHOLD['area']:
                        box['bndbox'] = {
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
