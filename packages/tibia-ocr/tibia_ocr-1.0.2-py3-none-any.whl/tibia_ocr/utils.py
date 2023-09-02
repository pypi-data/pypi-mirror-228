import hashlib

import cv2
import numpy as np


def crop(img, rect):
    """Crops an cv2 image using coordinate and size"""
    return img[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]


def get_hash(image):
    """Returns the hash of the image"""
    return hashlib.md5(image.tobytes()).hexdigest()


def get_diff(img1, img2):
    diff = cv2.absdiff(img1, img2)
    return np.sum(diff)
