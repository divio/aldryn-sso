#!/usr/bin/env python
HELPER_SETTINGS = {
    'INSTALLED_APPS': [],
    'SECRET_KEY': 'some-secret',
    'ALLOWED_HOSTS': ['localhost'],
}


def run():
    from app_helper import runner
    runner.run('aldryn_sso')


if __name__ == '__main__':
    run()
