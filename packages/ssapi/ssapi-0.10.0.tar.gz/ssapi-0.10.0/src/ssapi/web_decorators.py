import json
import sqlite3
from functools import wraps

from bottle import request, response, LocalResponse

from ssapi.defaults import DEFAULT_SSAPI_WEB_CONTENT_TYPE
from ssapi.web_tools import camel_to_snake_case

response: LocalResponse


def accepts_json(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        content_type = request.headers.get("content-type", None)
        if content_type in (DEFAULT_SSAPI_WEB_CONTENT_TYPE, None):
            if request.json is None:
                request.adapted_json = None
            else:
                try:
                    request.adapted_json = camel_to_snake_case(request.json)
                except json.JSONDecodeError as exc:
                    response.status = 400
                    return {"outcome": f"error: invalid JSON: {exc}"}
        else:
            response.status = 400
            return {"outcome": "error: accepts only application/json"}

        return callable(*args, **kwargs)

    return wrapper


def returns_json(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs) -> str:
        response.content_type = DEFAULT_SSAPI_WEB_CONTENT_TYPE
        return json.dumps(callable(*args, **kwargs))

    return wrapper


def handles_db_errors(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        try:
            return callable(*args, **kwargs)
        except sqlite3.Error as err:
            response.status = 500
            return {"outcome": f"error: db: {err}"}

    return wrapper


def enables_cors(callable):
    @wraps(callable)
    def wrapper(*args, **kwargs):
        response.add_header('Access-Control-Allow-Origin', '*')
        response.add_header(
            'Access-Control-Allow-Methods',
            'GET, POST, PUT, OPTIONS'
        )
        response.add_header(
            'Access-Control-Allow-Headers',
            'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
        )
        return callable(*args, **kwargs)

    return wrapper
