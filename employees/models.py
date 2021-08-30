from datetime import datetime
from hashlib import sha1
from os import environ
from typing import Any
from urllib.parse import urlencode

from django.core.files.uploadedfile import UploadedFile
from django.db import models
from requests import post

ENDPOINT = 'https://api.cloudinary.com/v1_1'


def upload(picture: UploadedFile) -> dict[str, Any]:
    return post(
        url='%s/%s/image/upload' % (ENDPOINT, environ.get('CLOUDINARY_CLOUD_NAME')),
        data=__build_body(),
        files={'file': picture},
    ).json()


def destroy(picture_id: str) -> dict[str, Any]:
    return post(
        url='%s/%s/image/destroy' % (ENDPOINT, environ.get('CLOUDINARY_CLOUD_NAME')),
        data=__build_body({
            'public_id': picture_id,
        }),
    ).json()


def __build_body(additional_params: dict[str, Any] = None) -> dict[str, Any]:
    if additional_params is None:
        additional_params = {}

    now = int(datetime.now().timestamp())
    secret = environ.get('CLOUDINARY_SECRET')

    params = additional_params | {'timestamp': str(now)}
    to_sign = map(lambda key: (key, params.get(key)), sorted(params.keys()))
    to_sign = dict(to_sign)
    to_sign = '%s%s' % (urlencode(to_sign), secret)
    signature = sha1(to_sign.encode('ascii')).hexdigest()

    signed_body = params | {
        'signature': signature,
        'api_key': environ.get('CLOUDINARY_API_KEY'),
    }

    return additional_params | signed_body


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    dob = models.DateField()
    permanent = models.BooleanField(default=False)
    picture_id = models.CharField(max_length=25, null=True)
    status = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        if self.picture_id is not None:
            self.del_picture()
        super().delete(*args, **kwargs)

    def set_picture(self, picture: UploadedFile) -> None:
        if self.picture_id is not None:
            self.del_picture()
        response = upload(picture)
        self.picture_id = response.get('public_id')
        self.save()

    def del_picture(self):
        response = destroy(self.picture_id)
        if response.get('result') == 'ok':
            self.picture_id = None
            self.save()
