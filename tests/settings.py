#!/usr/bin/env python
HELPER_SETTINGS = {
    'INSTALLED_APPS': [],
    'SECRET_KEY': 'some-secret',
    'ALLOWED_HOSTS': ['localhost'],
    'CMS_LANGUAGES': {
        1: [{
            'code': 'en',
            'name': 'English',
        }]
    },
    'LANGUAGE_CODE': 'en',
}


def run():
    from app_helper import runner
    try:
        runner.cms('aldryn_sso')
    except ImportError:
        runner.run('aldryn_sso')


if __name__ == '__main__':
    run()
