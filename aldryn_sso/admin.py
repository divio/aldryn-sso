# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.template.response import TemplateResponse


if settings.ALDRYN_SSO_HIDE_USER_MANAGEMENT:
    admin.site.unregister(User)
    admin.site.unregister(Group)


original_admin_login_view = admin.site.login


@login_required
def admin_login_view(request, extra_context=None):
    # The login required decorator takes care of redirect not logged in users
    # to our custom login view.
    # It does not make sense to show the admin login form for users that are
    # logged in, but are not staff users (default behaviour of admin).
    # Instead show an message and explain the situation to the user.
    if not request.user.is_staff:
        context = dict()
        return TemplateResponse(
            request,
            'aldryn_sso/admin_non_staff.html',
            context,
        )
    return original_admin_login_view(request, extra_context=extra_context)


if settings.ALDRYN_SSO_OVERIDE_ADMIN_LOGIN_VIEW:
    # force the default admin login view to use the default django login view
    admin.site.login = admin_login_view
