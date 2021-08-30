import json
from json.decoder import JSONDecodeError
from typing import Union, Optional

from django.http.request import HttpRequest


def json_middleware(get_response):
    def middleware(request: HttpRequest):
        if 'application/json' in request.headers.get('Content-Type', ''):
            try:
                request.json = json.loads(request.body)
            except JSONDecodeError:
                pass
        if not hasattr(request, 'json'):
            request.json = None
        response = get_response(request)
        return response

    return middleware


class AuthorizedJsonRequest(HttpRequest):
    json: Union[dict, list, str, int, float, bool, None] = None
    auth_user: Optional[str] = None
