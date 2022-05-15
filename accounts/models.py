from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """ WARNING : user_id is NOT the id of the user in the app but the id in the company system.
    Both are not correlated"""
    user_id = models.PositiveIntegerField(null=True, blank=True)


