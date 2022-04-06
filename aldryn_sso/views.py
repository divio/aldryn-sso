import django.contrib.auth
import django.contrib.auth.views
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, resolve_url


try:
    # Django <3.0
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme
    from django.utils.http import urlencode
except ImportError:
    # Django >=3.0
    from django.utils.http import url_has_allowed_host_and_scheme, urlencode

from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import CreateView

from .forms import AuthenticationForm, CreateUserForm, LoginAsForm


def get_shared_context():
    setting_keys = [
        'enable_sso_login',
        'enable_auto_sso_login',
        'enable_login_form',
        'enable_localdev',
    ]
    context = {}
    for key in setting_keys:
        key_name = 'aldryn_sso_{}'.format(key)
        value = getattr(settings, key_name.upper(), False)
        context[key_name] = value
        if key == 'enable_login_form':
            context['aldryn_sso_login_form'] = AuthenticationForm()
        elif key == 'enable_localdev':
            context['aldryn_sso_localdev_login_as_form'] = LoginAsForm()
    if not context['aldryn_sso_enable_sso_login']:
        context['aldryn_sso_enable_auto_sso_login'] = False
    return context


def get_next_from_request(request):
    redirect_to = request.POST.get(
        django.contrib.auth.REDIRECT_FIELD_NAME,
        request.GET.get(django.contrib.auth.REDIRECT_FIELD_NAME, '')
    )
    return redirect_to


def get_redirect_url(request, fallback=None):
    redirect_to = get_next_from_request(request)

    # Ensure the user-originating redirection url is safe.

    if not url_has_allowed_host_and_scheme(
        url=redirect_to,
        allowed_hosts=request.get_host(),
    ):
        redirect_to = None

    if not redirect_to and fallback:
        redirect_to = fallback
    return redirect_to


def login_as_user(request, next_page=None):
    if not next_page:
        fallback = resolve_url(settings.LOGIN_REDIRECT_URL)
        next_page = get_redirect_url(request, fallback=fallback)

    form = LoginAsForm(request.POST or None)

    if request.user.is_authenticated:
        response = HttpResponseRedirect(next_page)
    elif form.is_valid():
        django.contrib.auth.login(request, form.cleaned_data['user'])
        response = HttpResponseRedirect(next_page)
    else:
        context = {
            'aldryn_sso_localdev_login_as_form': form,
            django.contrib.auth.REDIRECT_FIELD_NAME: next_page
        }
        context.update(get_shared_context())
        response = render(request, 'aldryn_sso/login_screen.html', context)
    return response


class CreateUserView(CreateView):
    form_class = CreateUserForm
    template_name = 'aldryn_sso/create_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[django.contrib.auth.REDIRECT_FIELD_NAME] = get_next_from_request(self.request)
        return context

    def get_success_url(self):
        if self.request.user.is_authenticated:
            fallback = resolve_url(settings.LOGIN_REDIRECT_URL)
        else:
            fallback = reverse('aldryn_sso_localdev_login')
        return get_redirect_url(self.request, fallback=fallback)


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, **kwargs):
    kwargs['authentication_form'] = AuthenticationForm
    extra_context = kwargs.get('extra_context', {})
    extra_context.update(get_shared_context())
    kwargs['extra_context'] = extra_context
    if request.method == 'POST':
        return django.contrib.auth.views.LoginView.as_view(**kwargs)(request, **kwargs)
    next_url = get_redirect_url(
        request,
        fallback=resolve_url(settings.LOGIN_REDIRECT_URL),
    )
    if request.user.is_authenticated:
        # already authenticated. no sense in logging in.
        return HttpResponseRedirect(next_url)
    if (
        settings.ALDRYN_SSO_ENABLE_AUTO_SSO_LOGIN and
        settings.ALDRYN_SSO_ENABLE_SSO_LOGIN and not (
            settings.ALDRYN_SSO_ENABLE_LOCALDEV or
            settings.ALDRYN_SSO_ENABLE_LOGIN_FORM
        )
    ):
        # The aldryn SSO button would be the only thing on the page. So we just
        # initiate the login without further ado.
        sso_url = '{}?{}'.format(
            reverse('simple-sso-login'),
            urlencode(dict(next=next_url)),
        )
        return HttpResponseRedirect(sso_url)
    return django.contrib.auth.views.LoginView.as_view(**kwargs)(request, **kwargs)
