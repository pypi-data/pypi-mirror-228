from typing import Any, Dict
from requests import Response
from django.conf import settings
from vanoma_api_utils.http import client
from djangorestframework_camel_case.util import camelize  # type: ignore
from .exceptions import BackendServiceException


class AuthApiException(BackendServiceException):
    pass


def create_actor(data: Dict[str, Any]) -> Response:
    response = client.post(
        f"{settings.VANOMA_AUTH_API_URL}/actors",
        data=camelize(data),
    )

    if not response.ok:
        json = response.json()
        raise AuthApiException(
            response.status_code, json["error_code"], json["error_message"]
        )

    return response


def sign_in(data: Dict[str, Any]) -> Response:
    response = client.post(
        f"{settings.VANOMA_AUTH_API_URL}/sign-in",
        data=camelize(data),
    )

    if not response.ok:
        json = response.json()
        raise AuthApiException(
            response.status_code, json["error_code"], json["error_message"]
        )

    return response
