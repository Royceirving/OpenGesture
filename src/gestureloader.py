import os
import sys
import logging
import re
import cv2

from gesture import Gesture

logging.basicConfig(
    format="%(asctime)s [Loader] [%(levelname)s] %(message)s",
    level=logging.DEBUG
)

class GestureLoadManager:

    GESTURES_DIR = "temp"
    META_FILENAME = f"{GESTURES_DIR}/gesturedata.txt"
    META_PATTERN = re.compile(r"gesture(\d+).jpg\t(.*)")
    FILE_PATTERN = re.compile(r"gesture(\d+).jpg")

    def __init__(self) -> None:
        pass

    def load() -> list:
        try:
            files = os.listdir(GestureLoadManager.GESTURES_DIR)
        except FileNotFoundError:
            logging.debug("Temp directory not found")
            return []

        try:
            metadata_file = open(GestureLoadManager.META_FILENAME,'r')
        except FileNotFoundError:
            logging.debug(f"{GestureLoadManager.META_FILENAME} not found")
            return []

        for line in metadata_file:
            pass
        

    def save(gestures:list) -> None:
        try:
            os.mkdir(GestureLoadManager.GESTURES_DIR)
        except FileExistsError:
            pass

        metadata_file = open(GestureLoadManager.META_FILENAME,'w')
        logging.debug(f"Opened {GestureLoadManager.META_FILENAME}")

        file_counter = 0
        for gesture in gestures:
            filename = f"{GestureLoadManager.GESTURES_DIR}/gesture{file_counter}.jpg"
            cv2.imwrite(filename,gesture.gt_image)
            logging.debug(f"Saved {filename}")
            metadata_file.write(f"{filename}\t{gesture.command}\n")
            file_counter += 1

        metadata_file.close()
        logging.debug(f"Closed {GestureLoadManager.META_FILENAME}")
