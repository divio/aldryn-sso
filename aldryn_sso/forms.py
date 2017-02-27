# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, load_backend
import django.contrib.auth.forms
from django.utils.translation import ugettext_lazy as _


User = get_user_model()


class CreateUserForm(django.contrib.auth.forms.UserCreationForm):

    is_superuser = forms.BooleanField(initial=True, required=False)

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        del self.fields['password1']
        del self.fields['password2']

    def save(self, commit=True):
        # Use ModelForm save() directly
        # to avoid any behavior coming from UserCreationForm
        user = forms.ModelForm.save(self, commit=False)
        user.set_unusable_password()
        user.is_superuser = self.cleaned_data['is_superuser']
        user.is_active = True
        user.is_staff = True

        if commit:
            user.save()
        return user


class LoginAsForm(forms.Form):

    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True, is_staff=True),
        required=True,
    )

    def clean(self):
        user = self.cleaned_data.get('user')

        if not user:
            # let django handle the form error
            return self.cleaned_data

        for backend in settings.AUTHENTICATION_BACKENDS:
            auth_user = load_backend(backend).get_user(user.pk)

            if user == auth_user:
                user.backend = backend
                break

        if not hasattr(user, 'backend'):
            message = 'Unable to login as %(username)s' % {'username': user.username}
            raise forms.ValidationError(message)
        return self.cleaned_data


class AuthenticationForm(django.contrib.auth.forms.AuthenticationForm):
    error_messages = (
        django.contrib.auth.forms.AuthenticationForm.error_messages.copy()
    )
    error_messages['invalid_login_sso_hint'] = _(
        'Your Divio Account credentials will not work here, press the '
        '"Sign in with Divio Account" button instead.'
    )

    def clean(self):
        try:
            super(AuthenticationForm, self).clean()
        except forms.ValidationError as e:
            if (
                settings.ALDRYN_SSO_ENABLE_SSO_LOGIN and
                e.code == 'invalid_login'
            ):
                raise forms.ValidationError([
                    e,
                    forms.ValidationError(
                        self.error_messages['invalid_login_sso_hint'],
                        code='invalid_login_sso_hint',
                    )
                ])
            else:
                raise e
        return self.cleaned_data
