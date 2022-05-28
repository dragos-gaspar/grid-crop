import os

import xmltodict
from typing import Union


def make_dir(dir_path: str) -> Union[str, None]:
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


def read_voc(path: str) -> dict:
    """
    Get bounding boxes from xml files formatted in Pascal VOC format

    :param path: Path to xml file
    :return: list of bounding boxes
    """

    with open(path) as xml_file:
        data_dict = xmltodict.parse(xml_file.read())

    xml_file.close()
    bounding_boxes = data_dict["annotation"]

    return bounding_boxes
