# -*- coding: utf-8 -*-
"""
Login service user with cloud_id
"""
from __future__ import absolute_import, unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


from .managers import AldrynCloudUserManager

@python_2_unicode_compatible
class AldrynCloudUser(models.Model):
    cloud_id = models.PositiveIntegerField(unique=True)
    user = models.OneToOneField(
        User,
        unique=True,
        related_name='aldryn_cloud_account'
    )

    objects = AldrynCloudUserManager()

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = 'Aldryn SSO user'
        verbose_name_plural = 'Aldryn SSO users'


class AldrynSSOUser(AldrynCloudUser):
    """
    This is a Proxy model, so that we can change app_label and have admin show
    it together with the django.contrib.auth models.
    """
    class Meta:
        proxy = True
        app_label = 'auth'
        verbose_name = AldrynCloudUser._meta.verbose_name
        verbose_name_plural = AldrynCloudUser._meta.verbose_name_plural
