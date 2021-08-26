from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    dob = models.DateField()
    permanent = models.BooleanField(default=False)
    picture_id = models.CharField(max_length=25)
    status = models.IntegerField(default=0)
