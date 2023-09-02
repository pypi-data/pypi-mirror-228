import json
import os
from functools import lru_cache

import cv2
import numpy as np

from tibia_ocr.exceptions import FontNotFound
from tibia_ocr.utils import crop
from tibia_ocr.utils import get_hash


@lru_cache()
def get_model(font):
    try:
        dirname = os.path.dirname(__file__)
        with open(os.path.join(dirname, "fonts", font + ".json")) as fp:
            letters = json.load(fp)
            return {l["hash"]: l for l in letters}
    except FileNotFoundError:
        raise FontNotFound(f'Font "{font}" not found.')


@lru_cache()
def get_min_width(font):
    # returns the minimum width of a letter in the font
    model = get_model(font)
    min_width = min([l["width"] for l in model.values()])
    return min_width


@lru_cache()
def get_min_height(font):
    # returns the minimum height of a letter in the font
    model = get_model(font)
    min_height = min([l["height"] for l in model.values()])
    return min_height


def convert_letter(image, font="big", debug=False):
    """Ocr a letter"""
    model_obj = get_model(font)
    _, width = image.shape[:2]
    if width == 0:
        return ""
    min_tentative_width = get_min_width(font)
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
        letter = model_obj.get(letter_hash, None)
        if debug:
            cv2.imshow("", letter_image)
            cv2.setWindowTitle("", str(letter))
            if letter is not None:
                print(letter["letter"])
            cv2.waitKey()
            cv2.destroyWindow("")
        if letter is not None:
            remaining_image = image[:, tentative_width:]
            letter = letter["letter"]
            return letter + convert_letter(remaining_image, font=font)
    return ""


def convert_line(image, font="big", debug=False):
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
        letter = convert_letter(letter_image, font=font)
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


def convert_paragraph(image, font="big"):
    """Ocr a paragraph"""
    start = None
    paragraph = []
    for i, row in enumerate(image):
        non_zero = np.count_nonzero(row)
        if non_zero == 0 and start is not None:
            line = image[start:i]
            if line.shape[0] >= get_min_height(font):
                paragraph.append(convert_line(line, font=font))
            start = None
        if non_zero > 0 and start is None:
            start = i
    if start is not None:
        line = image[start:]
        if line.shape[0] >= get_min_height(font):
            paragraph.append(convert_line(line, font=font))
    return "\n".join(paragraph)
