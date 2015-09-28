# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url

from .sso import CloudUserClient


client = CloudUserClient.from_dsn(settings.SSO_DSN)

urlpatterns = patterns(
    '',
    url(r'^login/', include(client.get_urls())),
)
