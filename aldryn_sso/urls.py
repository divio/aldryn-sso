# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url

from .sso import CloudUserClient
from .views import CreateUserView, login_as_user

urlpatterns = []

if getattr(settings, 'LOCAL_DEVELOPMENT', False):
    urlpatterns += patterns(
        '',
        url(r'^create-user/$', CreateUserView.as_view(), name='aldryn_local_create_user'),
        url(r'^login-as/$', login_as_user, name='aldryn_local_login'),
    )

if getattr(settings, 'SSO_DSN', False):
    client = CloudUserClient.from_dsn(settings.SSO_DSN)
    urlpatterns += patterns('', url(r'^login/', include(client.get_urls())))
