import cv2

from tibia_ocr.hash_ocr import convert_line
from tibia_ocr.hash_ocr import convert_paragraph


def convert(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    return convert_line(image)


def convert_in_range(image, upper, lower):
    image = cv2.inRange(image, upper, lower)
    return convert_line(image)


def convert_red(image):
    return convert_in_range(image, (17, 17, 176), (255, 255, 255))


def convert_paragraph_in_range(image, upper, lower):
    image = cv2.inRange(image, upper, lower)
    return convert_paragraph(image)


def convert_number_threshed(image):
    try:
        return int(convert_line(image))
    except ValueError:
        return -1


def convert_number(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    return convert_number_threshed(image)


def convert_number_in_range(image, lower, upper):
    try:
        image = cv2.inRange(image, lower, upper)
        return int(convert_line(image))
    except ValueError:
        return -1


def convert_number_red(image):
    return convert_number_in_range(image, (17, 17, 176), (255, 255, 255))


def convert_number_green(image):
    return convert_number_in_range(image, (17, 170, 17), (255, 255, 255))
