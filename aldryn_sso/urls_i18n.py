# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib.auth import views as auth_views

from .views import CreateUserView, login_as_user, login

urlpatterns = []

if getattr(settings, 'ALDRYN_SSO_ENABLE_LOCALDEV', False):
    urlpatterns += patterns(
        '',
        url(r'^localdev/create-user/$', CreateUserView.as_view(), name='aldryn_localdev_create_user'),
        url(r'^localdev/login-as/$', login_as_user, name='aldryn_localdev_login'),
    )

urlpatterns += patterns(
    '',
    url(
        r'^login/$',
        login,
        kwargs=dict(
            template_name='aldryn_sso/login_screen.html',
        ),
        name='aldryn_sso_login',
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        name='aldryn_sso_logout',
    )
)
