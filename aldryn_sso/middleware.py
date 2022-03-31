"""
Access Control Middleware
"""
import base64
import logging
import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import NoReverseMatch, reverse
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import urlencode
from django.utils.translation import get_language_from_path


logger = logging.getLogger('aldryn-sso')


class BaseAccessControlMiddleware(MiddlewareMixin):
    # List of paths that will not trigger login mechanism
    # It can contain the following values:
    # /admin/.* -> regex
    # /path/ -> exact match
    # /en/some-path/ -> language prefixed
    # reverse_lazy('login') -> lazy url
    LOGIN_WHITE_LIST = settings.ALDRYN_SSO_LOGIN_WHITE_LIST

    def strip_language(self, path):
        language_prefix = get_language_from_path(path)

        if not language_prefix:
            return path
        # strip the language prefix by getting the length of the language
        # then slice the path
        return '/' + '/'.join(path.split('/')[2:])

    def can_skip_check(self, request):
        if getattr(request, '_login_exempt', False):
            # Apps can bypass auth check by setting the
            # _login_exempt attribute on the request to True.
            # This is useful for tests that make use of a fake request.
            return True

        if self.is_white_list_url(request):
            # skipping the authentication check
            return True

        if self.sharing_view_is_already_authed(request):
            # the user accessed the website with the sharing token,
            # skipping the authentication check
            return True
        return False

    def is_white_list_url(self, request):
        """
        Returns true if the request path matches a configured
        list of "white listed" url paths.
        """
        path = request.path_info

        if settings.APPEND_SLASH and not path.endswith('/'):
            path += '/'

        path_without_prefix = self.strip_language(request.path)

        for exclusive_path in self.LOGIN_WHITE_LIST:
            try:
                exclusive_path = str(exclusive_path)
            except NoReverseMatch:
                continue
            exclusive_path_without_prefix = self.strip_language(exclusive_path)

            if exclusive_path == path:
                return True
            elif exclusive_path_without_prefix == path_without_prefix:
                return True
            elif re.match(exclusive_path, path):
                return True
            elif re.match(exclusive_path_without_prefix, path_without_prefix):
                return True
        return False

    def sharing_view_is_already_authed(self, request):
        return bool(
            request.session.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME)
        )

    def sharing_view_init(self, request):
        # check if the user is using the "view only sharing url"
        secret_token = settings.SHARING_VIEW_ONLY_SECRET_TOKEN
        if secret_token:
            token = request.GET.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME, None)
            if secret_token == token:
                request.session[settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME] = token
                return HttpResponseRedirect(request.get_full_path())


class AccessControlMiddleware(BaseAccessControlMiddleware):
    login_template = 'aldryn_sso/login_screen.html'

    def process_request(self, request):
        if request.user.is_authenticated:
            # the user is already logged in
            return None

        if self.can_skip_check(request):
            return None

        sharing_view_response = self.sharing_view_init(request)

        if sharing_view_response:
            return sharing_view_response

        return self.render_login_page(request)

    def render_login_page(self, request):
        login_url = '{}?{}'.format(
            reverse('aldryn_sso_login'),
            urlencode(dict(next=request.path_info)),
        )
        return HttpResponseRedirect(login_url)


class BasicAuthAccessControlMiddleware(BaseAccessControlMiddleware):

    def unauthed(self, request):
        response = render(request, 'aldryn_sso/basicauth_auth_required.html', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Protected"'
        return response

    def process_request(self, request):
        if self.can_skip_check(request):
            return None

        sharing_view_response = self.sharing_view_init(request)

        if sharing_view_response:
            return sharing_view_response

        if 'HTTP_AUTHORIZATION' not in request.META:
            return self.unauthed(request)
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ', 1)
            if 'basic' != authmeth.lower():
                return self.unauthed(request)
            auth = base64.b64decode(auth.strip())
            if isinstance(auth, bytes):
                auth = auth.decode()
            username, password = auth.split(':', 1)
            if (
                username == settings.ALDRYN_SSO_BASICAUTH_USER and
                password == settings.ALDRYN_SSO_BASICAUTH_PASSWORD
            ):
                return

            return self.unauthed(request)
