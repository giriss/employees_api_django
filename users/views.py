from django.db.models import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST

from rest_api.json import AuthorizedJsonRequest
from .models import User


@require_POST
def create(request: AuthorizedJsonRequest) -> HttpResponse:
    try:
        user = User(**request.json['user'])
        user.save()
        return gen_response(user.gen_token())
    except IntegrityError:
        return JsonResponse({
            'errors': ['Username already taken']
        })


@require_POST
def login(request: AuthorizedJsonRequest) -> HttpResponse:
    params = request.json.get('user', {})
    username = params.get('username')
    password = params.get('password')
    try:
        user = User.objects.get(username=username)
        if user.check_password(password):
            return gen_response(user.gen_token())
    except ObjectDoesNotExist:
        pass
    return JsonResponse({
        'errors': ['Invalid username or password'],
    })


def gen_response(access_token: dict) -> JsonResponse:
    return JsonResponse({
        'data': {
            'access_token': access_token['token'],
            'exp': access_token['exp'],
        },
    })
