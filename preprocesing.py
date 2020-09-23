from io import BytesIO

import cv2
import numpy as np
from lxml import html
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


def captcha_preprocessing(svg_data: str) -> []:
    """
    Parsing SVG file body. remove useless element, save SVG as image
    :param svg_data: string with full svg data
    :return: image array
    """
    tree = html.fromstring(svg_data)
    svg_elements = tree.xpath("//svg/path[@fill!='none']")

    svg_images = []
    images = []

    for element in svg_elements:
        svg_image = ""
        svg_image += """<svg xmlns="http://www.w3.org/2000/svg" width="150" height="50" viewBox="0,0,150,50">"""
        svg_image += f"<path d='{element.attrib['d']}'></path>"
        svg_image += "</svg>"
        svg_images.append(svg_image)

    for svg_image in svg_images:
        with BytesIO(bytes(svg_image, "utf-8")) as buf:
            buf.seek(0)
            # prepare and save image
            drawing = svg2rlg(buf)
            renderPM.drawToFile(drawing, buf, fmt="PNG")
            buf.seek(0)
            # procesing image to array
            image = np.asarray(bytearray(buf.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)
            images.append(image)

    return images


def contours(image) -> list:
    """
    Update src image and cut each element
    :param image: src image
    :return: captcha image
    """

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # mask
    th, im_th = cv2.threshold(gray, 254, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    # contours
    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    cnt = cv2.boundingRect(sorted_contours[0])
    x, y, w, h = cnt
    new_img = image[y: y + h, x: x + w]
    # tresholding black to black and white to white
    new_img[new_img <= 250] = 0
    new_img[new_img > 250] = 255

    return cv2.resize(new_img, (20, 25))


import os
import string


import requests
import uuid

for x in range(150):
    resp = requests.get("https://mvd.gov.by/api/captcha/main?unique=1600816661182")
    data = resp.json()["data"]
    images = captcha_preprocessing(data)
    for image in images:
        image_boxed = contours(image)

        name = uuid.uuid4()

        cv2.imwrite(f"files/test/{name}_full.jpg", image)
        cv2.imwrite(f"files/test/{name}_boxed.jpg", image_boxed)

