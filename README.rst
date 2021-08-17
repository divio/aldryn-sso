==========
Aldryn SSO
==========

|build| |coverage|

**Aldryn SSO** adds single-sign-on to Divio Cloud.

This addon still uses the legacy "Aldryn" naming. You can read more about this in our
`support section <https://support.divio.com/general/faq/essential-knowledge-what-is-aldryn>`_.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-sso/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/aldryn-sso/blob/master/setup.py>`_
file for additional dependencies:

|python| |django|


Installation
------------

Nothing to do. ``aldryn-sso`` is part of the Divio Cloud.


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |build| image:: https://travis-ci.org/divio/aldryn-sso.svg?branch=master
    :target: https://travis-ci.org/divio/aldryn-sso
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-sso/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-sso

.. |python| image:: https://img.shields.io/badge/python-3.5+-blue.svg
    :target: https://pypi.org/project/aldryn-sso/
.. |django| image:: https://img.shields.io/badge/django-2.2,%203.0,%203.1-blue.svg
    :target: https://www.djangoproject.com/

Sharing Links and Tokens
------------------------

Aldryn SSO supports a "test link" or "preview mode" feature to bypass the password protection of test environments. This is normally useful to share a test environment with other people without complicated setups and passwords, a link is enough.

The links are in the following form: `https://{aldryn_url}/?sharing_token={token}`, where the token is the value of the `SHARING_VIEW_ONLY_SECRET_TOKEN` environment variable.

This environment variable can bet set in the container as part of your build process. The argument name (`sharing_token`) can also be overridden by setting the `SHARING_VIEW_ONLY_TOKEN_KEY_NAME` environment variable to your desired value.

