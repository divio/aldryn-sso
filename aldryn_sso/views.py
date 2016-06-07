# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django.conf import settings
import django.contrib.auth
import django.contrib.auth.views
from django.core.urlresolvers import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, render_to_response
from django.template import RequestContext
from django.utils.http import is_safe_url, urlencode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView

from .forms import CreateUserForm, LoginAsForm


def get_shared_context():
    context = {}
    if settings.ALDRYN_SSO_ENABLE:
        context.update({
            'aldryn_sso_enable': True,
        })
    if settings.ALDRYN_SSO_ENABLE_STANDARD_LOGIN:
        context.update({
            'aldryn_sso_standard_login_form': AuthenticationForm(),
            'aldryn_sso_enable_standard_login': True,
        })
    if settings.ALDRYN_LOCALDEV_ENABLE:
        context.update({
            'aldryn_localdev_login_as_form': LoginAsForm(),
            'aldryn_localdev_enable': True,
        })
    return context


def get_next_from_request(request):
    redirect_to = request.POST.get(
        django.contrib.auth.REDIRECT_FIELD_NAME,
        request.GET.get(django.contrib.auth.REDIRECT_FIELD_NAME, '')
    )
    return redirect_to


def get_redirect_url(request, fallback=None):
    # don't use request.REQUEST because it is deprecated.
    redirect_to = get_next_from_request(request)

    # Ensure the user-originating redirection url is safe.

    if not is_safe_url(url=redirect_to, host=request.get_host()):
        redirect_to = None

    if not redirect_to and fallback:
        redirect_to = fallback
    return redirect_to


def login_as_user(request, next_page=None):
    if not next_page:
        fallback = resolve_url(settings.LOGIN_REDIRECT_URL)
        next_page = get_redirect_url(request, fallback=fallback)

    form = LoginAsForm(request.POST or None)

    if request.user.is_authenticated():
        response = HttpResponseRedirect(next_page)
    elif form.is_valid():
        django.contrib.auth.login(request, form.cleaned_data['user'])
        response = HttpResponseRedirect(next_page)
    else:
        context = {
            'aldryn_localdev_login_as_form': form,
            django.contrib.auth.REDIRECT_FIELD_NAME: next_page
        }
        context.update(get_shared_context())
        response = render_to_response(
            'aldryn_sso/login_screen.html',
            context,
            context_instance=RequestContext(request)
        )
    return response


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'aldryn_sso/create_user.html'

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context[django.contrib.auth.REDIRECT_FIELD_NAME] = get_next_from_request(self.request)
        return context

    def get_success_url(self):
        if self.request.user.is_authenticated():
            fallback = resolve_url(settings.LOGIN_REDIRECT_URL)
        else:
            fallback = reverse('aldryn_localdev_login')
        return get_redirect_url(self.request, fallback=fallback)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, **kwargs):
    extra_context = kwargs.get('extra_context', {})
    extra_context.update(get_shared_context())
    kwargs['extra_context'] = extra_context
    if request.method == 'POST':
        return django.contrib.auth.views.login(request, **kwargs)
    next_url = get_redirect_url(
        request,
        fallback=resolve_url(settings.LOGIN_REDIRECT_URL),
    )
    if request.user.is_authenticated():
        # already authenticated. no sense in logging in.
        return HttpResponseRedirect(next_url)
    if (
        settings.ALDRYN_SSO_AUTO_LOGIN and
        settings.ALDRYN_SSO_ENABLE and not (
            settings.ALDRYN_LOCALDEV_ENABLE or
            settings.ALDRYN_SSO_ENABLE_STANDARD_LOGIN
        )
    ):
        # The aldryn SSO button would be the only thing on the page. So we just
        # initiate the login without further ado.
        sso_url = '{}?{}'.format(
            reverse('simple-sso-login'),
            urlencode(dict(next=next_url)),
        )
        return HttpResponseRedirect(sso_url)
    return django.contrib.auth.views.login(request, **kwargs)