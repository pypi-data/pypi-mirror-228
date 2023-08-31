import hashlib
import json
from functools import lru_cache

import cv2
import numpy as np


@lru_cache()
def _get_model():
    with open("assets/json/letters.json") as file_pointer:
        letters = json.load(file_pointer)
        return {l["hash"]: l["letter"] for l in letters}


def crop(img, rect):
    """Crops an cv2 image using coordinate and size"""
    return img[rect[1] : rect[1] + rect[3], rect[0] : rect[0] + rect[2]]


def get_hash(image):
    """Returns the hash of the image"""
    return hashlib.md5(image.tobytes()).hexdigest()


def convert_letter(image, debug=False):
    """Ocr a letter"""
    model = _get_model()
    _, width = image.shape[:2]
    if width == 0:
        return ""
    min_tentative_width = 2
    max_tentative_width = min(10, width)
    for tentative_width in reversed(
        range(min_tentative_width, max_tentative_width + 1)
    ):
        letter_image = image[:, :tentative_width]
        contours, _ = cv2.findContours(
            letter_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        if contours == []:
            continue
        letter_image = crop(letter_image, cv2.boundingRect(contours[0]))
        letter_hash = get_hash(letter_image)
        letter = model.get(letter_hash, None)
        if debug:
            cv2.imshow("", letter_image)
            cv2.setWindowTitle("", str(letter))
            if letter is not None:
                print(letter)
            cv2.waitKey()
        if letter is not None:
            remaining_image = image[:, tentative_width:]
            return letter + convert_letter(remaining_image)
    return ""


def convert_line(image, debug=False):
    """Ocr a line"""
    contours, _ = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = list(contours)
    contours.sort(key=lambda c: cv2.boundingRect(c)[0])
    line = ""
    for contour in contours:
        # create a mask from the contour
        mask = np.zeros_like(image)
        cv2.drawContours(mask, [contour], 0, 255, -1)

        # mask the original image
        letter_image = cv2.bitwise_and(image, mask)

        # crop the letter image and convert the image to character
        bounding_rect = cv2.boundingRect(contour)
        letter_image = crop(letter_image, bounding_rect)
        letter = convert_letter(letter_image)
        line += letter

        # debug
        if debug:
            cv2.imshow(
                letter,
                cv2.resize(letter_image, None, fx=30, fy=30, interpolation=0),
            )
            cv2.waitKey()
            cv2.destroyWindow(letter)
    return line


def convert_paragraph(image):
    """Ocr a paragraph"""
    start = None
    paragraph = []
    for i, row in enumerate(image):
        non_zero = np.count_nonzero(row)
        if non_zero == 0 and start is not None:
            line = image[start:i]
            if line.shape[0] >= 6:
                paragraph.append(convert_line(line))
            start = None
        if non_zero > 0 and start is None:
            start = i
    if start is not None:
        line = image[start:]
        if line.shape[0] >= 6:
            paragraph.append(convert_line(line))
    return "\n".join(paragraph)
