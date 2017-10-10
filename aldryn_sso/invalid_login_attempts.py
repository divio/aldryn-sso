# -*- coding: utf-8 -*-
import base64

from django.conf import settings
from django.core.cache import cache
from django.utils.functional import cached_property


# When feature is turned off INVALID_LOGIN_MAX_ATTEMPTS is None
INVALID_LOGIN_MAX_ATTEMPTS = getattr(settings, 'ALDRYN_SSO_INVALID_LOGIN_MAX_ATTEMPTS', 5)
INVALID_LOGIN_BLOCK_EXPIRATION_MIN = getattr(settings, 'ALDRYN_SSO_INVALID_LOGIN_BLOCK_EXPIRATION_MIN', 15)


class Counter:
    max_invalid_attempts = INVALID_LOGIN_MAX_ATTEMPTS
    invalid_attempts_expire_minutes = INVALID_LOGIN_BLOCK_EXPIRATION_MIN
    cache = cache

    def __init__(self, identifier):  # identifier => eg username or session-id
        self.identifier = identifier or '_no_session_key_'

    @classmethod
    def invalid_attempts_cache_key(cls, identifier):
        b64 = base64.b64encode(identifier.encode('utf-8'))
        return '_invalid_attempt_count_%s' % b64

    def reset(self):
        key = self.invalid_attempts_cache_key(self.identifier)
        self.cache.delete(key)

    def incr(self):
        key = self.invalid_attempts_cache_key(self.identifier)
        expiry = 60 * self.invalid_attempts_expire_minutes
        value = cache.get_or_set(key, 0, expiry)
        self.cache.set(key, value + 1, expiry)

    def too_many_attempts(self):
        if not self.identifier:
            return False
        key = self.invalid_attempts_cache_key(self.identifier)
        value = self.cache.get(key, 0)
        # we gonna substract 1 because counting starts after first wrong
        # attempt
        return value >= self.max_invalid_attempts - 1


# For cases when someone wishes the feature to be turned off:
class DummyCounter:
    def reset(self):
        pass

    def incr(self):
        pass

    def too_many_attempts(self):
        return False


class InvalidLoginAttemptsMixin(object):
    # Has to be mixed into something that has self.request. Like view or
    # AuthenticationForm

    @cached_property
    def invalid_login_counter(self):
        if not INVALID_LOGIN_MAX_ATTEMPTS:
            return DummyCounter()

        dummy_key = '_invalid_login_counter_dummy'
        if not self.request.session._session_key:
            # let's do something with session so that key gets populated...
            # https://stackoverflow.com/questions/12257116/django-when-is-sessionid-cookie-set-is-it-available-by-default
            self.request.session[dummy_key] = True
        elif dummy_key in self.request.session:
            # ...and then cleanup
            del self.request.session[dummy_key]
        return Counter(self.request.session._session_key)
