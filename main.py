import os
import re

import config
from crop import crop_image


# Append base paths in config
config.INPUT_PATHS = [os.path.join(config.INPUT_BASE, inp) for inp in config.INPUT_PATHS]


def main() -> None:
    """
    App entry point

    :return: None
    """

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
