from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, re_path

from .views import CreateUserView, login, login_as_user


urlpatterns = []

if getattr(settings, 'ALDRYN_SSO_ENABLE_LOCALDEV', False):
    urlpatterns += [
        re_path(r'^localdev/create-user/$', CreateUserView.as_view(), name='aldryn_localdev_create_user'),
        re_path(r'^localdev/login-as/$', login_as_user, name='aldryn_sso_localdev_login'),
    ]

prefix = getattr(settings, 'ALDRYN_SSO_LOGIN_URL_PREFIX', '')
if prefix:
    prefix = '{}/'.format(prefix)

urlpatterns += [
    re_path(r'^{}'.format(prefix), include([
        re_path(
            r'^login/$',
            login,
            kwargs={'template_name': 'aldryn_sso/login_screen.html'},
            name='aldryn_sso_login',
        ),
        re_path(
            r'^logout/$',
            auth_views.LogoutView.as_view(),
            name='aldryn_sso_logout',
        )
    ]))
]
