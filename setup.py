#!/usr/bin/env python
from setuptools import find_packages, setup

from aldryn_sso import __version__


REQUIREMENTS = [
    'aldryn-addons',
    'django-simple-sso>=0.14.0',
    'furl',
]


CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Framework :: Django',
    'Framework :: Django :: 2.2',
    'Framework :: Django :: 3.2',
    'Framework :: Django :: 4.2',
    'Framework :: Django :: 5',
    'Framework :: Django CMS',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development',
    'Topic :: Software Development :: Libraries',
]


setup(
    name='aldryn-sso',
    version=__version__,
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/divio/aldryn-sso',
    license='BSD-3-Clause',
    description='Single sign on integration for Divio Cloud.',
    long_description=open('README.rst').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    classifiers=CLASSIFIERS,
    test_suite='tests.settings.run',
)
