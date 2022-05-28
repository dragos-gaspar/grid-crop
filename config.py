# Directory that contains the dataset (absolute path)
INPUT_BASE = r"D:\Facultate\Master An 1\PCD2\Plastic-Bottles-Dataset"


# List of directories that contain images (relative to INPUT_BASE);
INPUT_PATHS = [
    r"001-Sindangbarang River, Bogor, Indonesia-eka",
    r"002-Cisadane River, Bogor, Indonesia-eka"
]


# Image output directory. Can be any directory (absolute path or relative to cwd)
# Directories in the INPUT_PATHS list will be created here if they don't exist
IMAGES_OUTPUT_PATH = r"processed_images"


# Annotations output directory. Can be any directory (absolute path or relative to cwd)
# Directories in the INPUT_PATHS list will be created here if they don't exist
ANNOTATIONS_OUTPUT_PATH = r"processed_annotations"


# Size of resulting cropped images
CROP_WIDTH = 576
CROP_HEIGHT = 532


# Bounding box thresholding; a resulting bounding box in a crop must satisfy these minimum requirements
THRESHOLD = {
    'height': 10,
    'width': 10,
    'area': 200
}


# Format of the resulting annotations; can be "json" for "voc"
ANNOTATIONS_FORMAT = 'xml'
