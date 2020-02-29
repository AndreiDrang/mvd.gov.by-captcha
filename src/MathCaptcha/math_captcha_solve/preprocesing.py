from io import BytesIO

import cv2
import numpy as np
from lxml import html
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


def captcha_preprocessing(svg_data: str) -> np.array:
    """
    Parsing SVG file body. remove useless element, save SVG as image
    :param svg_data: string with full svg data
    :return: image array
    """
    tree = html.fromstring(svg_data)
    svg_elements = tree.xpath("//svg/path[@fill!='none']")

    svg_image = ""
    svg_image += """<svg xmlns="http://www.w3.org/2000/svg" width="150" height="50" viewBox="0,0,150,50">"""
    for element in svg_elements:
        svg_image += f"<path d='{element.attrib['d']}'></path>"
    svg_image += "</svg>"

    with BytesIO(bytes(svg_image, "utf-8")) as buf:
        buf.seek(0)
        # prepare and save image
        drawing = svg2rlg(buf)
        renderPM.drawToFile(drawing, buf, fmt="PNG")
        buf.seek(0)
        # procesing image to array
        image = np.asarray(bytearray(buf.read()), dtype="uint8")
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        return image


def contours(image) -> list:
    """
    Update src image and cut each element
    :param image: src image
    :return: list with captcha elements images
    """
    result = []

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # mask
    th, im_th = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY_INV)
    im_floodfill = im_th.copy()
    h, w = im_th.shape[:2]
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0, 0), 255)
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    # Combine the two images to get the foreground.
    im_out = im_th | im_floodfill_inv

    # contours
    contours, hierarchy = cv2.findContours(im_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # boxes draw
    boxes = []
    for cnt in sorted_contours[:3]:
        boxes.append(cv2.boundingRect(cnt))

    ordered_boxes = sorted(boxes, key=lambda x: x[0])
    for idx, (x, y, w, h) in enumerate(ordered_boxes):
        new_img = image[y : y + h, x : x + w]
        # tresholding black to black and white to white
        new_img[new_img <= 220] = 0
        new_img[new_img > 220] = 255

        result.append(cv2.resize(new_img, (20, 25)))

    return result
