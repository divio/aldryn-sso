# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.models import User, Group


if settings.ALDRYN_SSO_HIDE_USER_MANAGEMENT:
    admin.site.unregister(User)
    admin.site.unregister(Group)
