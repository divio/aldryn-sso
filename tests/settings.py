HELPER_SETTINGS = {
    'ALDRYN_SSO_OVERIDE_ADMIN_LOGIN_VIEW': False,
    'ALDRYN_SSO_ALWAYS_REQUIRE_LOGIN': 'basicauth',
    'ALDRYN_SSO_BASICAUTH_USER': 'user',
    'ALDRYN_SSO_BASICAUTH_PASSWORD': 'pass',
    'ALDRYN_SSO_HIDE_USER_MANAGEMENT': False,
    'ALDRYN_SSO_LOGIN_WHITE_LIST': [],
    'SHARING_VIEW_ONLY_TOKEN_KEY_NAME': 'randomunicorn',
    'SHARING_VIEW_ONLY_SECRET_TOKEN': 'randomunicorn',

    'MIDDLEWARE_CLASSES': [
        'django.middleware.gzip.GZipMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',

        'aldryn_sso.middleware.BasicAuthAccessControlMiddleware',

        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.contrib.sites.middleware.CurrentSiteMiddleware',
        'aldryn_sites.middleware.SiteMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware'
    ],

    'INSTALLED_APPS': [
        'aldryn_sites',
    ],
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_sso')


if __name__ == '__main__':
    run()
