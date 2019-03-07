from django.contrib.auth.views import AuthenticationForm, SetPasswordForm
from django.contrib.auth.forms import UsernameField, UserCreationForm, password_validation
from django.forms import EmailField
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model
from django import forms

User = get_user_model()


class UserLoginForm(AuthenticationForm):

    username = UsernameField(
        label='Username or email address',
        max_length=50,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )

    password = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput,
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "The two password fields didn't match."
    }
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )

    class Meta:
        model = User
        fields = ("username", 'email')
        field_classes = {'username': UsernameField, 'email': EmailField}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exits():
            raise forms.ValidationError(
                self.error_messages['email_exists'],
                code='email_exists',
            )
        return email


class UserResetPasswordForm(SetPasswordForm):

    error_messages = {
        'password_mismatch': "The two password fields didn't match.",
    }
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label="New password confirmation",
        strip=False,
        widget=forms.PasswordInput,
    )

