import django.contrib.auth.forms
from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model, load_backend
from django.contrib.auth.hashers import make_password
from django.utils.text import capfirst
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _


UserModel = get_user_model()


class CreateUserForm(forms.Form):
    username = forms.CharField(max_length=254)
    is_superuser = forms.BooleanField(initial=True, required=False)

    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = capfirst(self.username_field.verbose_name)

    def save(self, commit=True):
        # We want to use UserModel.objects.create_superuser and
        # UserModel.objects.create_user because developers that have their own
        # user models are likely to override them.

        user_kwargs = {
            UserModel.USERNAME_FIELD: self.cleaned_data.pop('username'),
            'password': make_password(None)
        }

        email_field = getattr(UserModel, 'EMAIL_FIELD', 'email')
        if email_field not in user_kwargs:
            user_kwargs[email_field] = None
        if self.cleaned_data.get('is_superuser', None):
            return UserModel.objects.create_superuser(**user_kwargs)
        else:
            user = UserModel.objects.create_user(**user_kwargs)
            user.is_staff = True
            user.save()
            return user


class LoginAsForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=UserModel.objects.filter(is_active=True, is_staff=True),
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
            message = gettext('Unable to login as %(username)s')
            raise forms.ValidationError(message % {'username': user.username})
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
            super().clean()
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
