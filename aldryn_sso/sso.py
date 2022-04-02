import json

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse

from furl import furl
from simple_sso.sso_client.client import AuthenticateView, Client, LoginView

from .models import AldrynCloudUser


User = get_user_model()

ALDRYN_USER_SESSION_KEY = '_aldryn_user'
IS_AJAX_URLPARAM = '__is_xhr_login'


class QuickerExpirationAuthenticateView(AuthenticateView):

    def options(self, request):
        response = super().options(request)
        response['Access-Control-Allow-Origin'] = 'null'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With'
        return response

    def get(self, request):
        response = super().get(request)
        request.session[ALDRYN_USER_SESSION_KEY] = True
        request.session.set_expiry(settings.CLOUD_USER_SESSION_EXPIRATION)
        request.session.save()

        # request.is_ajax() does not work for xhr redirects :-(
        next_url = self.get_next()
        next_url = furl(next_url)
        is_ajax = bool(next_url.args.pop(IS_AJAX_URLPARAM, False))
        if is_ajax and request.user.is_authenticated:
            # Return JSON response so JS can detect that the login was
            # successful.
            response = HttpResponse(
                json.dumps({
                    'is_authenticated': True,
                    'next': next_url.url,
                }),
                content_type="application/json",
            )
            # If the token were not valid, we'd never get here. So it is safe
            # to set very open CORS headers.
            # 'null' because that is what most browsers send as "Origin" after a
            # xhr redirect from an different domain.
            response['Access-Control-Allow-Origin'] = 'null'
            response['Access-Control-Allow-Credentials'] = 'true'
            return response
        response['Location'] = next_url.url
        return response


class TryLoginView(LoginView):
    """
    Same as normal login view, adds a indicator so that it is still possible
    to identify this as an ajax request after all the redirects.
    """
    def is_ajax(self):
        return self.request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

    def get_next(self):
        next_url = furl(super().get_next())
        if self.is_ajax():
            next_url.args[IS_AJAX_URLPARAM] = 1
        return next_url.url


class CloudUserClient(Client):
    login_view = TryLoginView
    authenticate_view = QuickerExpirationAuthenticateView
    user_extra_data = ['cloud_id']

    def _get_free_username(self, original_username):
        username = original_username
        i = 1
        while User.objects.filter(**{User.USERNAME_FIELD: username}).exists():
            username = u'%s - %s' % (original_username, i)
            i += 1
        return username

    def _create_user(self, username, email):
        username = self._get_free_username(username)
        email_field = getattr(User, 'EMAIL_FIELD', 'email')
        return User.objects.create(**{User.USERNAME_FIELD: username, email_field: email})

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
            user_email = user_data.pop('email')
            user = User.objects.filter(email=user_email).first()
            if user:
                AldrynCloudUser.objects.create(cloud_id=cloud_id, user=user)
            else:
                user = self._create_user(
                    username=username,
                    email=user_email,
                )
        else:
            user = account.user

        for key, value in user_data.items():
            setattr(user, key, value)

        user.set_unusable_password()
        user.save()
        return user
