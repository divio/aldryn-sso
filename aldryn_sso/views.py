# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url, render_to_response
from django.template import RequestContext
from django.utils.http import is_safe_url
from django.views.generic import CreateView

from .forms import CreateUserForm, LoginAsForm


def get_next_from_request(request):
    redirect_to = request.POST.get(
        REDIRECT_FIELD_NAME,
        request.GET.get(REDIRECT_FIELD_NAME, '')
    )
    return redirect_to


def get_redirect_url(request, fallback=None):
    # don't use request.REQUEST
    # is deprecated
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
        login(request, form.cleaned_data['user'])
        response = HttpResponseRedirect(next_page)
    else:
        context = {
            'CMSCLOUD_STATIC_URL': settings.CMSCLOUD_STATIC_URL,
            'form': form,
            REDIRECT_FIELD_NAME: next_page
        }
        response = render_to_response(
            'aldryn_sso/login_screen_local.html',
            context,
            context_instance=RequestContext(request)
        )
    return response


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'aldryn_sso/create_user.html'

    def get_context_data(self, **kwargs):
        context = super(CreateUserView, self).get_context_data(**kwargs)
        context['CMSCLOUD_STATIC_URL'] = settings.CMSCLOUD_STATIC_URL
        context[REDIRECT_FIELD_NAME] = get_next_from_request(self.request)
        return context

    def get_success_url(self):
        if self.request.user.is_authenticated():
            fallback = resolve_url(settings.LOGIN_REDIRECT_URL)
        else:
            fallback = reverse('aldryn_local_login')
        return get_redirect_url(self.request, fallback=fallback)
