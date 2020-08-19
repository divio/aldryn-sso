from django.conf import settings
from django.urls import include, re_path

from .sso import CloudUserClient


urlpatterns = []

if getattr(settings, 'ALDRYN_SSO_ENABLE_SSO_LOGIN', False):
    client = CloudUserClient.from_dsn(settings.SSO_DSN)
    urlpatterns += [re_path(r'^aldryn_sso/login/', include(client.get_urls()))]
