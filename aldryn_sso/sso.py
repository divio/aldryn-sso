# -*- coding: utf-8 -*-
import json
import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.conf.urls import url
from django.http import HttpResponse
from furl import furl

from simple_sso.sso_client.client import Client, AuthenticateView, LoginView

from .models import AldrynCloudUser


ALDRYN_USER_SESSION_KEY = '_aldryn_user'
IS_AJAX_URLPARAM = '__is_xhr_login'


class QuickerExpirationAuthenticateView(AuthenticateView):

    def get(self, request):
        response = super(QuickerExpirationAuthenticateView, self).get(request)
        request.session[ALDRYN_USER_SESSION_KEY] = True
        request.session.set_expiry(settings.CLOUD_USER_SESSION_EXPIRATION)
        request.session.save()

        # request.is_ajax() does not work for xhr redirects :-(
        next = self.get_next()
        next = furl(next)
        is_ajax = bool(next.args.pop(IS_AJAX_URLPARAM, False))
        if is_ajax and request.user.is_authenticated():
            # return JSON response so JS can detect that the login was
            # successful.
            response = HttpResponse(
                json.dumps({
                    'is_authenticated': True,
                    'next': next.url,
                }),
                content_type="application/json",
            )
            # if the token were not valid, we'd never get to here. So it is safe
            # to set very open CORS headers here.
            # 'null' because that is what most browsers send as "Origin" after a
            # xhr redirect from a other domain.
            response['Access-Control-Allow-Origin'] = 'null'
            response['Access-Control-Allow-Credentials'] = 'true'
            return response
        response['Location'] = next.url
        return response  # redirects to "next"


class TryLoginView(LoginView):
    """
    Same as normal login view, adds a indicator so that it is still possible
    to identify this as an ajax request after all the redirects.
    """
    def get_next(self):
        next = super(TryLoginView, self).get_next()
        next = furl(next)
        if self.request.is_ajax():
            next.args[IS_AJAX_URLPARAM] = 1
        return next.url


class CloudUserClient(Client):
    login_view = TryLoginView
    authenticate_view = QuickerExpirationAuthenticateView
    user_extra_data = ['cloud_id']

    def _get_free_username(self, original_username):
        username = original_username
        i = 1
        while User.objects.filter(username=username).exists():
            username = u'%s - %s' % (original_username, i)
            i += 1
        return username

    def _create_user(self, username, email):
        username = self._get_free_username(username)
        return User.objects.create(username=username, email=email)

    def build_user(self, user_data):
        extra_data = user_data.pop('extra_data')

        cloud_id = extra_data['cloud_id']

        # It's important that username is removed
        # from the user_data dictionary because the dictionary
        # is used to update the existing user object.
        username = user_data.pop('username')

        try:
            account = AldrynCloudUser.objects.get(cloud_id=cloud_id)
        except AldrynCloudUser.DoesNotExist:
            user = self._create_user(
                username=username,
                email=user_data.pop('email'),
            )

            AldrynCloudUser.objects.create(cloud_id=cloud_id, user=user)
        else:
            user = account.user

        for key, value in user_data.items():
            setattr(user, key, value)

        user.set_unusable_password()
        user.save()
        return user
