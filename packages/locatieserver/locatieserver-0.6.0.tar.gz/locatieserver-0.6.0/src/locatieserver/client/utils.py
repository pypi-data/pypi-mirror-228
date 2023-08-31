import inspect
from typing import Any
from typing import Callable
from typing import Dict

import httpx
from httpx import Response
from httpx._types import QueryParamTypes

from locatieserver.client.config import BASE_URL
from locatieserver.schema.error import ErrorResponse


DEFAULT_CACHE = {}


def get_defaults_from_function(func: Callable[..., Any]) -> Dict[str, Any]:
    if func.__name__ not in DEFAULT_CACHE:
        signature = inspect.signature(func)
        DEFAULT_CACHE[func.__name__] = {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }

    return DEFAULT_CACHE[func.__name__]


def filter_defaults(func: Callable[..., Any], **kwargs: Any) -> Dict[str, Any]:
    defaults = get_defaults_from_function(func)

    non_default_values = {}

    for key, value in kwargs.items():
        if key not in defaults or value != defaults[key]:
            non_default_values[key] = value

    return non_default_values


class LocatieserverError(Exception):
    pass


class LocatieserverResponseError(LocatieserverError):
    pass


def http_get(path: str, params: QueryParamTypes) -> Response:
    response = httpx.get(
        BASE_URL + path, params=params, headers={"accept": "application/json"}
    )

    if response.status_code == 200:
        return response
    else:
        if (
            "content-type" not in response.headers
            or response.headers["content-type"] != "application/json"
        ):
            raise LocatieserverResponseError(response.text)
        error_response = ErrorResponse.model_validate(response.json())

        raise LocatieserverResponseError(error_response.msg)
