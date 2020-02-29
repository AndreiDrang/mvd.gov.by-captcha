import time
from uuid import uuid4
from io import BytesIO

import requests
from lxml import html
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


PREPARED_FOLDER = "files/examples/"


def captcha_downloader():
    """
    Download captcha for tests
    """
    for _ in range(1500):
        resp = requests.get("https://mvd.gov.by/api/captcha/main?unique=1582836990084")
        data = resp.json()["data"]

        tree = html.fromstring(data)
        svg_elements = tree.xpath("//svg/path[@fill!='none']")

        svg_image = ""
        svg_image += """<svg xmlns="http://www.w3.org/2000/svg" width="150" height="50" viewBox="0,0,150,50">"""
        for element in svg_elements:
            svg_image += f"<path d='{element.attrib['d']}'></path>"
        svg_image += "</svg>"

        with BytesIO(bytes(svg_image, "utf-8")) as buf:
            buf.seek(0)

            drawing = svg2rlg(buf)
            renderPM.drawToFile(drawing, f"{PREPARED_FOLDER}{uuid4()}.png", fmt="PNG")

    time.sleep(0.9)
