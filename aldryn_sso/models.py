# -*- coding: utf-8 -*-
"""
Login service user with cloud_id
"""
from django.contrib.auth.models import User
from django.db import models

from .managers import AldrynCloudUserManager


class AldrynCloudUser(models.Model):
    cloud_id = models.PositiveIntegerField(unique=True)
    user = models.OneToOneField(
        User,
        unique=True,
        related_name='aldryn_cloud_account'
    )

    objects = AldrynCloudUserManager()
