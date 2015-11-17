# -*- coding: utf-8 -*-
from functools import partial

from aldryn_client import forms


class Form(forms.BaseForm):
    hide_user_management = forms.CheckboxField(
        'Hide user management',
        required=False,
        initial='true'
    )

    def to_settings(self, data, settings):
        from django.core.urlresolvers import reverse_lazy

        from aldryn_addons.utils import djsenv

        env = partial(djsenv, settings=settings)

        settings['LOGIN_REDIRECT_URL'] = '/'

        is_local_dev = env('STAGE') == 'local'
        if is_local_dev:
            settings['LOCAL_DEVELOPMENT'] = True

        if env('SSO_DSN'):
            # Expire user session every day because:
            # User can change its data on Login's server.
            # We cannot do a sync of "recently changed" user data due to these reasons:
            # - security risk, leaking user data to unauthorized websites,
            # - it would require some periodic tasks (celery?),
            # - stage websites are being paused during which the sync wouldn't work
            settings['CLOUD_USER_SESSION_EXPIRATION'] = 24 * 60 * 60  # 24h = 1day
            settings['SSO_DSN'] = env('SSO_DSN')

        if env('SSO_DSN') or is_local_dev:
            settings['ALDRYN_SSO_HIDE_USER_MANAGEMENT'] = data['hide_user_management']
            settings['ADDON_URLS'].append('aldryn_sso.urls')
            settings['INSTALLED_APPS'].insert(
                settings['INSTALLED_APPS'].index('django.contrib.admin'),
                'aldryn_sso'
            )
            settings['CMSCLOUD_STATIC_URL'] = env('CMSCLOUD_STATIC_URL', 'https://static.aldryn.com/')
        else:
            # there is no SSO_DSN set and is not local dev.
            # No point in configuring anything else.
            return settings

        if env('STAGE') == 'test':
            position = settings['MIDDLEWARE_CLASSES'].index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1
            settings['ALDRYN_SSO_LOGIN_WHITE_LIST'] = [reverse_lazy('simple-sso-login')]
            settings['MIDDLEWARE_CLASSES'].insert(position, 'aldryn_sso.middleware.AccessControlMiddleware')
            settings['SHARING_VIEW_ONLY_TOKEN_KEY_NAME'] = env('SHARING_VIEW_ONLY_TOKEN_KEY_NAME')
            settings['SHARING_VIEW_ONLY_SECRET_TOKEN'] = env('SHARING_VIEW_ONLY_SECRET_TOKEN')
        return settings
