# -*- coding: utf-8 -*-
"""
Login service user with cloud_id
"""
from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import AldrynCloudUserManager


@python_2_unicode_compatible
class AldrynCloudUser(models.Model):
    cloud_id = models.PositiveIntegerField(
        unique=True,
        verbose_name=_('Cloud ID'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        unique=True,
        verbose_name=_('User'),
        related_name='aldryn_cloud_account',
        on_delete=models.CASCADE,
    )

    objects = AldrynCloudUserManager()

    def __str__(self):
        return '{}'.format(self.user)

    class Meta:
        verbose_name = _('Aldryn SSO user')
        verbose_name_plural = _('Aldryn SSO users')
