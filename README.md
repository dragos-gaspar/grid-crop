# grid-crop
This tool takes a set of images and crops them according to a grid. The size of the grid cells can be set in the config.py file, along with other parameters.
The app is designed to work with the [Plastic Bottle Dataset](https://github.com/m0-n/Plastic-Bottles-Dataset), so it will expect a similar format for the
annotations. The annotations of the resulting cropped images are saved in json format.

## How to run
1. Clone this repository
```
git clone https://github.com/dragos-gaspar/grid-crop.git
```
2. Install the dependencies in a Python 3.9 environment
```
pip3 install -r requirements.txt
```
3. Edit config.py to add your desired parameters
4. Run the main.py script
```
python3 main.py
```
