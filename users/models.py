from datetime import datetime
from typing import Optional

from bcrypt import hashpw, checkpw, gensalt
from django.db import models
from jwt import encode

from rest_api.settings import SECRET_KEY


class User(models.Model):
    username = models.CharField(unique=True, max_length=200)
    password_hash = models.CharField(max_length=100)
    password: Optional[str] = None

    def __init__(self, *args, **kwargs) -> None:
        try:
            password: str = kwargs['password']
            del kwargs['password']
            super().__init__(*args, **kwargs)
            self.set_password(password)
        except KeyError:
            super().__init__(*args, **kwargs)

    def set_password(self, password: str) -> None:
        digest = hashpw(password.encode('utf-8'), gensalt())
        self.password_hash = digest.decode('utf-8')

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def save(self, *args, **kwargs):
        if self.password is not None:
            self.set_password(self.password)
        super().save(*args, **kwargs)

    def gen_token(self) -> dict[str, any]:
        exp = int(datetime.now().timestamp()) + 7_200
        token = encode(
            payload={
                'username': self.username,
                'exp': exp,
            },
            key=SECRET_KEY,
        )
        return {'token': token, 'exp': exp}
