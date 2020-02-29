import os

import cv2
import numpy as np
from numpy import dot, mean
from numpy.linalg import norm

VERTICAL_LINES = (7, 9, 11, 15, 18, 21)
HORIZONTAL_LINES = (9, 11, 15, 18)


def lines_counter() -> dict:
    res = {}
    path = "files/clustered/"
    folders = os.listdir(path)
    for folder in folders:
        res[folder] = []
        files = os.listdir(path + folder)
        for f in files:
            # imread ond processing
            img = cv2.imread(f"{path}{folder}/{f}", 0)
            img[img <= 220] = False
            img[img > 220] = True

            res[folder].append(img)
    return res


lines = lines_counter()


def predictor(image: np.array) -> str:
    results = {}

    bool_image = image.copy()
    bool_image[image <= 220] = False
    bool_image[image > 220] = True

    for key, images in lines.items():
        v_res = []
        h_res = []

        for image in images:
            for line in HORIZONTAL_LINES:
                h_res.append(
                    np.nan_to_num(
                        dot(image[:, line], bool_image[:, line])
                        / (norm(image[:, line]) * norm(bool_image[:, line]))
                    )
                )
            for line in VERTICAL_LINES:
                v_res.append(
                    np.nan_to_num(
                        dot(image[line, :], bool_image[line, :])
                        / (norm(image[line, :]) * norm(bool_image[line, :]))
                    )
                )

        v_mean = mean(v_res)
        h_mean = mean(h_res)

        r_max = round(max([v_mean, h_mean]), 2)

        results[key] = r_max

    if results is None:
        return None
    else:
        predict = max(results, key=lambda key: results[key])
        return predict
