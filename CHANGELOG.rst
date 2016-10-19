CHANGELOG
=========

1.1.5 (2016-10-19)
------------------

* add optional basic auth protection


1.1.4 (2016-09-07)
------------------

* Correctly enforce login for URLs containing locale identifiers with territory codes.


1.1.3 (2016-06-23)
------------------

* fix css linking non-existing files (fails with manifest static file storage)

1.1.2 (2016-06-22)
------------------

* bugfixes for auto SSO login


1.1.1 (2016-06-21)
------------------

* bugfixes for new login view
* instant ajax SSO login if user is already signed in on the sso server


1.1.0 (2016-06-07)
------------------

* optionally allow form based username/password logins
* separate settings to enable login methods (form, sso and localdev)
* all static media served from within the app
  (no longer relies on static.aldryn.com for css)
* if SSO is the only option, redirect straight to the login procedure instead of
  showing a screen with a single button to press.


1.0.14 (2016-05-29)
-------------------

* Fix faulty default for "hide user management" setting


1.0.13 (2016-05-24)
-------------------

* When creating a localdev user, the superuser box is now checked by default


1.0.12 (2016-05-11)
-------------------

* Fix an error in the redirect middleware preventing infinite redirects if ``SHARING_VIEW_ONLY_TOKEN_KEY_NAME`` is not set
* Fix a bug when using Python 3


1.0.11 (2016-04-29)
-------------------

* Change default of ``hide_user_management`` to ``False``


1.0.10 (2016-04-22)
-------------------

* Update login screen text


1.0.9 (2016-02-02)
------------------

* Keep initial request path and next parameters during login


1.0.8 (2015-11-23)
------------------

* Fix IntegrityError triggered by the SSO client.


1.0.7 (2015-11-19)
------------------

* Fix typo in class name of a toolbar item so it looks correctly in django CMS 3.2+


1.0.6 (2015-11-17)
------------------

* Adds appropriate classes to the template so it looks correctly in django CMS 3.2+


1.0.5 (2015-11-16)
------------------

* Add Django migrations for Django 1.7+


1.0.0 (2015-xx-xx)
------------------

Initial release
