# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views


from .sso import CloudUserClient

urlpatterns = []

if getattr(settings, 'ALDRYN_SSO_ENABLE', False):
    client = CloudUserClient.from_dsn(settings.SSO_DSN)
    urlpatterns += patterns('', url(r'^aldryn_sso/login/', include(client.get_urls())))
