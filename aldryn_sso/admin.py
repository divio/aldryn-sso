from django.conf import settings
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .models import AldrynCloudUser


User = get_user_model()


class AldrynCloudUserAdmin(admin.ModelAdmin):
    list_display = (
        'cloud_id',
        'linked_user',
    )
    search_fields = (
        'cloud_id',
        'user__username',
        'user__first_name',
        'user__last_name',
        'user__email',
    )
    raw_id_fields = (
        'user',
    )

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related('user')
        )

    def linked_user(self, obj):
        html_link = '<a href="{}">{}</a>'.format(
            reverse('admin:auth_user_change', args=[obj.pk]),
            obj.user,
        )
        return mark_safe(html_link)
    linked_user.short_description = _('User')
    # This can be removed once support for django < 2.0 is dropped
    linked_user.allow_tags = True
    linked_user.admin_order_field = 'user'


if getattr(settings, 'ALDRYN_SSO_HIDE_USER_MANAGEMENT', False):
    try:
        admin.site.unregister(User)
    except NotRegistered:
        pass
    admin.site.unregister(Group)
else:
    admin.site.register(AldrynCloudUser, AldrynCloudUserAdmin)


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


if getattr(settings, 'ALDRYN_SSO_OVERIDE_ADMIN_LOGIN_VIEW', False):
    # Force the default admin login view to use the default django login view.
    admin.site.login = admin_login_view
