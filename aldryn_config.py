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

        settings['ALDRYN_SSO_HIDE_USER_MANAGEMENT'] = data['hide_user_management']
        settings['ADDON_URLS'].append('aldryn_sso.urls')
        settings['INSTALLED_APPS'].append('aldryn_sso')
        settings['CMSCLOUD_STATIC_URL'] = env('CMSCLOUD_STATIC_URL')

        # Expire user session every day because:
        # User can change its data on Login's server.
        # We cannot do a sync of "recently changed" user data due to these reasons:
        # - security risk, leaking user data to unauthorized websites,
        # - it would require some periodic tasks (celery?),
        # - stage websites are being paused during which the sync wouldn't work
        settings['CLOUD_USER_SESSION_EXPIRATION'] =  24 * 60 * 60  # 24h = 1day
        settings['SSO_DSN'] = env('SSO_DSN')

        if env('STAGE') == 'test':
            position = settings['MIDDLEWARE_CLASSES'].index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1
            settings['ALDRYN_SSO_LOGIN_WHITE_LIST'] = [reverse_lazy('simple-sso-login')]
            settings['MIDDLEWARE_CLASSES'].insert(position, 'aldryn_sso.middleware.AccessControlMiddleware')
            settings['SHARING_VIEW_ONLY_TOKEN_KEY_NAME'] = env('SHARING_VIEW_ONLY_TOKEN_KEY_NAME')
            settings['SHARING_VIEW_ONLY_SECRET_TOKEN'] = env('SHARING_VIEW_ONLY_SECRET_TOKEN')
        return settings
