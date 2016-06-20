# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

from aldryn_sso import __version__


setup(
    name="aldryn-sso",
    version=__version__,
    description='Aldryn single sign on integration.',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/aldryn/aldryn-sso',
    packages=find_packages(),
    install_requires=(
        'aldryn-addons',
        'django-simple-sso',
        'furl',
    ),
    include_package_data=True,
    zip_safe=False,
)
