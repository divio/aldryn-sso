# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group


if settings.ALDRYN_SSO_HIDE_USER_MANAGEMENT:
    admin.site.unregister(User)
    admin.site.unregister(Group)

if settings.ALDRYN_SSO_OVERIDE_ADMIN_LOGIN_VIEW:
    # force the default admin login view to use the default django login view
    admin.site.login = login_required(admin.site.login)