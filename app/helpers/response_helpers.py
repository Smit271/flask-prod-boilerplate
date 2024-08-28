# app/helpers/response_helpers.py

from flask import jsonify


def success_response(data=None, msg="Success", status_code=200):
    response = {
        "status": True,
        "status_code": status_code,
        "data": data,
        "msg": msg
    }
    return jsonify(response), status_code


def error_response(msg="An error occurred", status_code=400, data=None):
    response = {
        "status": False,
        "status_code": status_code,
        "data": data,
        "msg": msg
    }
    return jsonify(response), status_code
