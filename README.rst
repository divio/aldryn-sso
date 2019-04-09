==========
Aldryn SSO
==========

|pypi| |build| |coverage|

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


.. |pypi| image:: https://badge.fury.io/py/aldryn-sso.svg
    :target: http://badge.fury.io/py/aldryn-sso
.. |build| image:: https://travis-ci.org/divio/aldryn-sso.svg?branch=master
    :target: https://travis-ci.org/divio/aldryn-sso
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-sso/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-sso

.. |python| image:: https://img.shields.io/badge/python-2.7%20%7C%203.4+-blue.svg
    :target: https://pypi.org/project/aldryn-sso/
.. |django| image:: https://img.shields.io/badge/django-1.11%20%7C%202.1%20%7C%202.2-blue.svg
    :target: https://www.djangoproject.com/
