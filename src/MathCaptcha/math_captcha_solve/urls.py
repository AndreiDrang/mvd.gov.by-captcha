import logging

from flask import Blueprint, request
from flask_api import status

from .preprocesing import captcha_preprocessing, contours
from .recognition import predictor

logger = logging.getLogger(__name__)

bp = Blueprint("math-captcha", __name__, url_prefix="/math-captcha")


@bp.route("/recognition", methods=["POST", "PUT"])
def recognition():
    response = {"result": "ok", "data": ""}

    if request.is_json:
        result_json = request.get_json()
        try:
            image = captcha_preprocessing(result_json["data"])
            resp = contours(image)
            first, sign, second = predictor(resp[0]), predictor(resp[1]), predictor(resp[2])
            response["data"] = f"{first} {sign} {second}"

            return response, status.HTTP_200_OK
        except Exception:
            logger.exception("While captcha recognition error occurred")

            response["result"] = "error"
            return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        response["result"] = "error"
        return response, status.HTTP_204_NO_CONTENT


@bp.route("/solve", methods=["POST", "PUT"])
def solve():
    response = {"result": "ok", "data": ""}

    if request.is_json:
        result_json = request.get_json()
        try:
            image = captcha_preprocessing(result_json["data"])
            resp = contours(image)
            first, sign, second = predictor(resp[0]), predictor(resp[1]), predictor(resp[2])
            result = eval(f"{first} {sign} {second}")
            response["data"] = result

            return response, status.HTTP_200_OK
        except Exception:
            logger.exception("While captcha recognition error occurred")

            response["result"] = "error"
            return response, status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        response["result"] = "error"
        return response, status.HTTP_204_NO_CONTENT
