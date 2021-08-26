from typing import Optional

from django.http.request import HttpRequest
from django.http.response import JsonResponse
from jwt import decode, InvalidTokenError

from rest_api.settings import SECRET_KEY


def authenticate_request(func):
    def inner(request: HttpRequest, *args, **kwargs):
        token: str = request.headers.get('authorization', '').removeprefix('Bearer ')
        try:
            username: Optional[str] = decode(token, SECRET_KEY, ['HS256']).get('username')
            request.auth_user = username
            return func(request, *args, **kwargs)
        except InvalidTokenError:
            return JsonResponse(
                data={
                    'errors': [
                        'Invalid auth token',
                    ],
                },
                status=401,
            )

    return inner
