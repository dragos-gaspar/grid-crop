# Directory that contains the dataset (absolute path)
INPUT_BASE = r"D:\Facultate\Master An 1\PCD2\Plastic-Bottles-Dataset"


# List of directories that contain images (relative to INPUT_BASE);
INPUT_PATHS = [
    r"001-Sindangbarang River, Bogor, Indonesia-eka",
]


# Output directory. Can be any directory (absolute path or relative to cwd)
OUTPUT_PATH = r"processed_images"


# Size of resulting cropped images
CROP_WIDTH = 576
CROP_HEIGHT = 532


# Bounding box thresholding; a resulting bounding box in a crop must satisfy these requirements
THRESHOLD = {
    'height': 10,
    'width': 10,
    'area': 200
}
