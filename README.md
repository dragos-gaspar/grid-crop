# grid-crop
This tool takes a set of images and crops them according to a grid. The size of the grid cells can be set in the config.py file, along with [other parameters](https://github.com/dragos-gaspar/grid-crop#how-to-use-configpy-parameters-guide).
The app is designed to work with the [Plastic Bottle Dataset](https://github.com/m0-n/Plastic-Bottles-Dataset), so it will expect the annotations to be in the Pascal VOC format. The annotations of the resulting cropped images
can be saved either as json or xml.

## How to run
1. Clone this repository
```
git clone https://github.com/dragos-gaspar/grid-crop.git
```
2. Install the dependencies in a Python 3.9 environment using pip (or using your preferred package manager)
```
pip3 install -r requirements.txt
```
3. Edit config.py to add your desired parameters
4. Run the main.py script
```
python main.py
```
## How to use (config.py parameters guide)
- Replace the path in <samp>INPUT_BASE</samp> with the path to the Plastic Bottles Dataset repository on your machine
- Add the names of the directories which contain the images you want to crop to the <samp>INPUT_PATHS</samp> list
- Set the <samp>OUTPUT_PATH</samp> variable. The same directory structure that can be found in the Plastic Bottles Dataset repo will be created at this path
#### Additional parameters
- <samp>CROP_WIDTH</samp> and <samp>CROP_HEIGHT</samp> control the size of the cropped images.
- <samp>THRESHOLD</samp> contains the cues used to determine if a bounding box is "valid". When a bounding box of a cropped image is created, the app checks if
the minimum requirements declared here are met. If they are not met then the bounding box is discarded. This is done in order to circumvent a corner case where only a few pixels of a bounding box overlap with the crop.
- <samp>ANNOTATIONS_FORMAT</samp> is the format for the resulting annotation files. Can be either "json" or "voc".