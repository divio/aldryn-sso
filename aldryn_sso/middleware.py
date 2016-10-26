# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
import logging
import re
import sys
import base64

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch, reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.http import urlencode
from django.utils.translation import get_language_from_path


logger = logging.getLogger('aldryn-sso')

if sys.version_info < (3,):
    cast_to_str = unicode
else:
    cast_to_str = str


class BaseAccessControlMiddleware(object):
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
        return "/" + "/".join(path.split("/")[2:])

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
                exclusive_path = cast_to_str(exclusive_path)
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
                return HttpResponseRedirect('/')


class AccessControlMiddleware(BaseAccessControlMiddleware):
    login_template = 'aldryn_sso/login_screen.html'

    def process_request(self, request):
        if request.user.is_authenticated():
            # the user is already logged in
            return None
        if self.is_white_list_url(request):
            # skipping the authentication check
            return None
        if self.sharing_view_is_already_authed(request):
            # the user accessed the website with the sharing token,
            # skipping the authentication check
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
        response = TemplateResponse(
            request=request,
            template='aldryn_sso/basicauth_auth_required.html',
            content_type='text/html',

        )
        response['WWW-Authenticate'] = 'Basic realm="Protected"'
        response.status_code = 401
        return response

    def process_request(self, request):
        if self.is_white_list_url(request):
            # skipping the authentication check
            return None
        if self.sharing_view_is_already_authed(request):
            # the user accessed the website with the sharing token,
            # skipping the authentication check
            return None
        sharing_view_response = self.sharing_view_init(request)
        if sharing_view_response:
            return sharing_view_response

        if not 'HTTP_AUTHORIZATION' in request.META:
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

