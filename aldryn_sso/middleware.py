# -*- coding: utf-8 -*-
"""
Access Control Middleware
"""
import logging
import re

from django.conf import settings
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import get_language_from_path

logger = logging.getLogger('aldryn-sso')


class AccessControlMiddleware(object):
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
        return "/" + "/".join(path.split("/")[len(language_prefix):])

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
            exclusive_path = unicode(exclusive_path)
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

    def process_request(self, request):
        if request.user.is_authenticated():
            # the user is already logged in
            return None
        if self.is_white_list_url(request):
            # skipping the authentication check
            return None
        if request.session.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME):
            # the user accessed the website with the sharing token,
            # skipping the authentication check
            return None

        # check if the user is using the "view only sharing url"
        token = request.GET.get(settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME, None)

        if settings.SHARING_VIEW_ONLY_SECRET_TOKEN == token:
            request.session[settings.SHARING_VIEW_ONLY_TOKEN_KEY_NAME] = token
            return HttpResponseRedirect('/')
        return TemplateResponse(request, 'aldryn_sso/login_screen.html')
