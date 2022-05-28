import os

import xmltodict
from typing import Union


def make_dir(dir_path: str) -> Union[str, None]:
    """
    Create a directory if it does not exist

    :param dir_path: absolute path to the directory
    :return: path to the directory if successful or None if and error occurred
    """

    split_path = os.path.split(dir_path)
    crt_path = ''

    for level in split_path:
        try:
            crt_path = os.path.join(crt_path, level)
            isdir = os.path.isdir(crt_path)
            if not isdir:
                os.mkdir(crt_path)

        except Exception as error:
            print(error)
            return None

    return crt_path


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
