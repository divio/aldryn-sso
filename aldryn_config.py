# -*- coding: utf-8 -*-
from aldryn_client import forms


class Form(forms.BaseForm):
    hide_user_management = forms.CheckboxField(
        'Hide user management',
        required=False,
        initial=False,
    )

    def to_settings(self, data, settings):
        from functools import partial
        from django.core.urlresolvers import reverse_lazy
        from aldryn_addons.exceptions import ImproperlyConfigured
        from aldryn_addons.utils import boolean_ish
        from aldryn_addons.utils import djsenv

        def add_template_context_processor(settings, processor):
            if 'TEMPLATE_CONTEXT_PROCESSORS' in settings:
                settings['TEMPLATE_CONTEXT_PROCESSORS'].append(processor)
            if 'TEMPLATES' in settings and len(settings['TEMPLATES']):
                template_settings = settings['TEMPLATES'][0]
                template_settings.setdefault('OPTIONS', {})
                template_settings['OPTIONS'].setdefault('context_processors', [])
                template_settings['OPTIONS']['context_processors'].append(processor)

        env = partial(djsenv, settings=settings)

        settings['ALDRYN_SSO_HIDE_USER_MANAGEMENT'] = data['hide_user_management']
        settings['SSO_DSN'] = env('SSO_DSN')

        settings['LOGIN_REDIRECT_URL'] = '/'

        settings['ALDRYN_SSO_ENABLE'] = boolean_ish(
            env(
                'ALDRYN_SSO_ENABLE',
                default=boolean_ish(settings['SSO_DSN']),
            )
        )

        settings['ALDRYN_SSO_ENABLE_STANDARD_LOGIN'] = boolean_ish(
            env(
                'ALDRYN_SSO_ENABLE_STANDARD_LOGIN',
                default=not settings['ALDRYN_SSO_HIDE_USER_MANAGEMENT'],
            )
        )

        settings['ALDRYN_LOCALDEV_ENABLE'] = boolean_ish(
            env(
                'ALDRYN_LOCALDEV_ENABLE',
                default=env('STAGE') == 'local',
            )
        )

        settings['ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN'] = boolean_ish(
            env(
                'ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN',
                default=env('STAGE') == 'test',
            )
        )

        settings['ALDRYN_SSO_LOGIN_WHITE_LIST'] = env(
            'ALDRYN_SSO_LOGIN_WHITE_LIST',
            default=[]
        )

        settings['ADDON_URLS'].append('aldryn_sso.urls')
        settings['ADDON_URLS_I18N'].append('aldryn_sso.urls_i18n')

        # aldryn_sso must be after django.contrib.admin so it can unregister
        # the User/Group Admin if necessary.
        settings['INSTALLED_APPS'].insert(
            settings['INSTALLED_APPS'].index('django.contrib.admin'),
            'aldryn_sso'
        )

        # FIXME: CMSCLOUD_STATIC_URL must be removed
        settings['CMSCLOUD_STATIC_URL'] = env('CMSCLOUD_STATIC_URL', 'https://static.aldryn.com/')

        if settings['ALDRYN_SSO_ENABLE']:
            # Expire user session every day because:
            # Users can change their data on the SSO server.
            # We cannot do a sync of "recently changed" user data due to these reasons:
            # - security risk, leaking user data to unauthorized websites,
            # - it would require some periodic tasks (celery?),
            # - stage websites are being paused during which the sync wouldn't work
            settings['CLOUD_USER_SESSION_EXPIRATION'] = 24 * 60 * 60  # 24h = 1day
            if not settings['SSO_DSN']:
                raise ImproperlyConfigured(
                    'ALDRYN_SSO_ENABLE is True, but no SSO_DSN is set.')
            add_template_context_processor(
                settings,
                'aldryn_sso.context_processors.sso_login'
            )

        if settings['ALDRYN_SSO_ENABLE_STANDARD_LOGIN']:
            add_template_context_processor(
                settings,
                'aldryn_sso.context_processors.standard_login',
            )

        if settings['ALDRYN_LOCALDEV_ENABLE']:
            add_template_context_processor(
                settings,
                'aldryn_sso.context_processors.local_development'
            )

        if settings['ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN']:
            position = settings['MIDDLEWARE_CLASSES'].index('django.contrib.auth.middleware.AuthenticationMiddleware') + 1
            settings['MIDDLEWARE_CLASSES'].insert(position, 'aldryn_sso.middleware.AccessControlMiddleware')
            settings['ALDRYN_SSO_LOGIN_WHITE_LIST'].append(reverse_lazy('simple-sso-login'))
            settings['SHARING_VIEW_ONLY_TOKEN_KEY_NAME'] = env('SHARING_VIEW_ONLY_TOKEN_KEY_NAME')
            settings['SHARING_VIEW_ONLY_SECRET_TOKEN'] = env('SHARING_VIEW_ONLY_SECRET_TOKEN')

        settings['ALDRYN_SSO_OVERIDE_LOGIN_VIEW'] = any([
            settings['ALDRYN_SSO_ENABLE'],
            settings['ALDRYN_SSO_ENABLE_STANDARD_LOGIN'],
            settings['ALDRYN_LOCALDEV_ENABLE'],
        ])

        if settings['ALDRYN_SSO_OVERIDE_LOGIN_VIEW']:
            # configure our combined login view to be the default
            settings['LOGIN_URL'] = 'aldryn_sso_login'
            # see admin.py for how we force admin to use this view as well
        return settings
