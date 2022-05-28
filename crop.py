import os
import json

import xmltodict
from skimage import io

import config
from utils import make_dir, read_voc


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
    annotation_data = read_voc(os.path.join(input_path, image_meta[1]))

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
            objects_out = []
            for obj in annotation_data['object']:
                # Cast bb coordinates to int
                bb = obj['bndbox']
                bb = {k: int(v) for k, v in bb.items()}

                # Calculate intersection sides' lengths
                dx = min(crop_rect['xmax'], bb['xmax']) - max(crop_rect['xmin'], bb['xmin'])
                dy = min(crop_rect['ymax'], bb['ymax']) - max(crop_rect['ymin'], bb['ymin'])

                # Check if intersection actually occurs
                if dx >= 0 and dy >= 0:
                    # Thresholding
                    if dx >= config.THRESHOLD['width'] and dy >= config.THRESHOLD['height'] \
                            and dx*dy >= config.THRESHOLD['area']:
                        out_box = {
                            'xmin': max(crop_rect['xmin'], bb['xmin']) - crop_offset_x,
                            'ymin': max(crop_rect['ymin'], bb['ymin']) - crop_offset_y,
                            'xmax': min(crop_rect['xmax'], bb['xmax']) - crop_offset_x,
                            'ymax': min(crop_rect['ymax'], bb['ymax']) - crop_offset_y
                        }
                        out_obj = obj.copy()
                        out_obj['bndbox'] = out_box
                        objects_out.append(out_obj)

            # Construct names
            base_name = f"{os.path.splitext(image_meta[0])[0]}_{(i * w_grid + j):03d}"
            crop_name = f"{base_name}.jpg"
            annotation_name = f"{base_name}.json" if config.ANNOTATIONS_FORMAT == 'json' else f"{base_name}.xml"
            full_crop_name = os.path.join(
                    make_dir(
                        os.path.join(
                            config.OUTPUT_PATH,
                            os.path.basename(input_path)
                        )
                    ),
                    crop_name
                )
            full_annotation_name = os.path.join(
                make_dir(
                    os.path.join(
                        config.OUTPUT_PATH,
                        os.path.basename(input_path)
                    )
                ),
                annotation_name
            )

            print(f"Saving {base_name}...")

            # Construct output annotation structure
            annotation_out = annotation_data.copy()
            annotation_out['object'] = objects_out
            annotation_out['filename'] = crop_name
            annotation_out['size'] = {
                'width': crop.shape[0],
                'height': crop.shape[1],
                'depth': crop.shape[2]
            }
            annotation_out = {'annotation': annotation_out}

            # Save image
            io.imsave(full_crop_name, crop, check_contrast=False)

            # Save annotation in configured format
            if config.ANNOTATIONS_FORMAT == 'json':
                # Save to json
                with open(full_annotation_name, 'w') as f:
                    json.dump(annotation_out, f)

            else:
                # Save to xml
                with open(full_annotation_name, 'w') as f:
                    xmltodict.unparse(annotation_out, f, pretty=True)
