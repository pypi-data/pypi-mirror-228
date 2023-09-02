import cv2

from tibia_ocr.hash_ocr import convert_line
from tibia_ocr.hash_ocr import convert_paragraph


def convert(image, font="big"):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    return convert_line(image, font=font)


def convert_in_range(image, upper, lower, font="big"):
    image = cv2.inRange(image, upper, lower)
    return convert_line(image, font=font)


def convert_red(image, font="big"):
    return convert_in_range(image, (17, 17, 176), (255, 255, 255), font=font)


def convert_paragraph_in_range(image, upper, lower, font="big"):
    image = cv2.inRange(image, upper, lower)
    return convert_paragraph(image, font=font)


def convert_number_threshed(image, font="big"):
    try:
        return int(convert_line(image, font=font))
    except ValueError:
        return -1


def convert_number(image, font="big"):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
    return convert_number_threshed(image, font=font)


def convert_number_in_range(image, lower, upper, font="big"):
    try:
        image = cv2.inRange(image, lower, upper)
        return int(convert_line(image, font=font))
    except ValueError:
        return -1


def convert_number_red(image, font="big"):
    return convert_number_in_range(
        image, (17, 17, 176), (255, 255, 255), font=font
    )


def convert_number_green(image, font="big"):
    return convert_number_in_range(
        image, (17, 170, 17), (255, 255, 255), font=font
    )
