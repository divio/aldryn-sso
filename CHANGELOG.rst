=========
Changelog
=========


2.0.1 (2021-08-17)
==================

* Added support for django-simple-sso >= 1.0 (stop depending on `simple_sso.compat`)


2.0.0 (2020-08-31)
==================

* Added support for Django 3.1
* Dropped support for Python 2.7 and Python 3.4
* Dropped support for Django < 2.2
* Prevent the login page from being indexed
* Fixed an error where emails get duplicated


1.7.0 (2020-01-29)
==================

* Added support for Django 3.0


1.6.0 (2019-04-09)
==================

* Added support for Django 2.2 and django CMS 3.7
* Removed support for Django 2.0
* Added test matrix
* Adapted code base to align with other supported addons


1.5.1 (2018-12-15)
==================

* Fixed a bug with middleware for Django 1.11


1.5.0 (2018-11-27)
==================

* Removed support for Django < 1.11


1.4.5 (2018-10-25)
==================

* Fixed a bug for new user creation on django<1.11


1.4.4 (2018-10-24)
==================

* Fixed a bug with ManifestGZippedStaticFilesStorage


1.4.3 (2018-10-19)
==================

* Pin ``itsdangerous`` to < 1


1.4.2 (2018-10-15)
==================

* Updated styles


1.4.1 (2018-10-15)
==================

* Updated styles


1.4.0 (2018-10-13)
==================

* New design
* Fixed auto-login


1.3.1 (2018-07-12)
==================

* Fixed compatibility with Django >= 1.11 on old-style classes.


1.3.0 (2018-04-04)
==================

* Introduced Django 2.0 support


1.2.1 (2018-02-16)
==================

* Fixed ContentNotRenderedError on Django 1.11


1.2.0 (2017-12-01)
==================

* Added support for custom User models


1.1.16 (2017-05-28)
===================

* Added a missing migration for a minor non-schema related change


1.1.15 (2017-04-28)
===================

* Added support for a ``_login_exempt`` attribute on the request.
  When set to ``True``, this attribute prevents the request from going through
  the authentication check.


1.1.14 (2017-03-02)
===================

* Added German translations
* Setup Transifex


1.1.13 (2017-02-28)
===================

* Added Django 1.10 support


1.1.12 (2017-01-26)
===================

* Redirect to same url after sharing token session init


1.1.11 (2016-12-21)
===================

* Removed the ``AldrynSSOUser`` proxy model to avoid migration issues.


1.1.10 (2016-12-02)
===================

* fix narrow font and button color


1.1.9 (2016-11-17)
==================

* rename Aldryn -> Divio


1.1.8 (2016-10-26)
==================

* fix another python3 issue in basic auth middleware


1.1.7 (2016-10-26)
==================

* fix python3 issue in basic auth middleware


1.1.6 (2016-10-19)
==================

* make url prefix of sso login/logout configurable through ``ALDRYN_SSO_LOGIN_URL_PREFIX``
* fix: add missing migration
* remove deprecated usage of ``pattern`` in urls


1.1.5 (2016-10-19)
==================

* add optional basic auth protection


1.1.4 (2016-09-07)
==================

* Correctly enforce login for URLs containing locale identifiers with territory codes.


1.1.3 (2016-06-23)
==================

* fix css linking non-existing files (fails with manifest static file storage)

1.1.2 (2016-06-22)
==================

* bugfixes for auto SSO login


1.1.1 (2016-06-21)
==================

* bugfixes for new login view
* instant ajax SSO login if user is already signed in on the sso server


1.1.0 (2016-06-07)
==================

* optionally allow form based username/password logins
* separate settings to enable login methods (form, sso and localdev)
* all static media served from within the app
  (no longer relies on static.aldryn.com for css)
* if SSO is the only option, redirect straight to the login procedure instead of
  showing a screen with a single button to press.


1.0.14 (2016-05-29)
===================

* Fix faulty default for "hide user management" setting


1.0.13 (2016-05-24)
===================

* When creating a localdev user, the superuser box is now checked by default


1.0.12 (2016-05-11)
===================

* Fix an error in the redirect middleware preventing infinite redirects if ``SHARING_VIEW_ONLY_TOKEN_KEY_NAME`` is not set
* Fix a bug when using Python 3


1.0.11 (2016-04-29)
===================

* Change default of ``hide_user_management`` to ``False``


1.0.10 (2016-04-22)
===================

* Update login screen text


1.0.9 (2016-02-02)
==================

* Keep initial request path and next parameters during login


1.0.8 (2015-11-23)
==================

* Fix IntegrityError triggered by the SSO client.


1.0.7 (2015-11-19)
==================

* Fix typo in class name of a toolbar item so it looks correctly in django CMS 3.2+


1.0.6 (2015-11-17)
==================

* Adds appropriate classes to the template so it looks correctly in django CMS 3.2+


1.0.5 (2015-11-16)
==================

* Add Django migrations for Django 1.7+


1.0.0 (2015-xx-xx)
==================

* Initial release
