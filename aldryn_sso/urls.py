# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, url

from .sso import CloudUserClient


urlpatterns = []

if getattr(settings, 'ALDRYN_SSO_ENABLE_SSO_LOGIN', False):
    client = CloudUserClient.from_dsn(settings.SSO_DSN)
    urlpatterns += [url(r'^aldryn_sso/login/', include(client.get_urls()))]
