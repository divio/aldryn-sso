# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginAsForm


def sso_login(request):
    return {
        'aldryn_sso_enable': True,
    }


def standard_login(request):
    return {
        'aldryn_sso_standard_login_form': AuthenticationForm(),
        'aldryn_sso_enable_standard_login': True,
    }


def local_development(request):
    return {
        'aldryn_localdev_login_as_form': LoginAsForm(),
        'aldryn_localdev_enable': True,
    }