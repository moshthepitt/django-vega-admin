"""Forms module for users"""
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.conf import settings

from crispy_forms.bootstrap import Field
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

from vega_admin.utils import get_form_actions

try:
    # pylint: disable=import-error
    from allauth.account import app_settings
    from allauth.account.adapter import get_adapter
except ModuleNotFoundError:
    UNIQUE_EMAIL = False
else:
    UNIQUE_EMAIL = app_settings.UNIQUE_EMAIL


class UserFormMixin:  # pylint: disable=too-few-public-methods
    """User forms mixin"""

    def clean_email(self):
        """clean email address"""
        value = self.cleaned_data['email']
        try:
            value = get_adapter().clean_email(value)
        except NameError:
            pass
        if value and UNIQUE_EMAIL:
            value = self.validate_unique_email(value)
        return value


class AddUserForm(UserFormMixin, forms.ModelForm):
    """
    Form class to add users
    """

    password = forms.CharField(
        label=_("Password"),
        strip=True,
        help_text=password_validation.password_validators_help_text_html()
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        """init method for add user form"""
        self.request = kwargs.pop('request', None)
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['username'].required = False
        self.fields['username'].help_text = _(settings.VEGA_USERNAME_HELP_TEXT)
        self.fields['email'].help_text = _(settings.VEGA_OPTIONAL_TXT)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'add-user-form'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('username'),
            Field('email'),
            Field('password', autocomplete="off"),
            Field('is_active'),
            get_form_actions(
                cancel_url=self.vega_extra_kwargs.get("cancel_url", "/")),
        )

    def clean_password(self):
        """clean password field"""
        data = self.cleaned_data['password']
        user = User()
        if self.cleaned_data.get('first_name'):
            user.first_name = self.cleaned_data['first_name']
        if self.cleaned_data.get('last_name'):
            user.last_name = self.cleaned_data['last_name']
        if self.cleaned_data.get('email'):
            user.email = self.cleaned_data['email']
        password_validation.validate_password(password=data, user=user)
        return data

    def validate_unique_email(self, value):  # pylint: disable=no-self-use
        """validate unique email while adding users"""
        try:
            return get_adapter().validate_unique_email(value)
        except NameError:
            return value

    def clean(self):
        """General clean method"""
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        if not email and not username:
            raise forms.ValidationError(
                _(settings.VEGA_EMAIL_OR_USERNAME_REQUIRED_TXT))

    def save(self, commit=True):
        """general form save method"""
        unique_username = self.cleaned_data.get("username")
        if not unique_username:
            try:
                unique_username = get_adapter().generate_unique_username([
                    self.cleaned_data.get('first_name'),
                    self.cleaned_data.get('last_name'),
                    self.cleaned_data.get('email'),
                ])
            except NameError:
                unique_username = self.cleaned_data.get('email')
        user_data = dict(username=unique_username,
                         first_name=self.cleaned_data['first_name'],
                         last_name=self.cleaned_data['last_name'],
                         password=self.cleaned_data['password'],
                         )
        if self.cleaned_data.get('email'):
            user_data['email'] = self.cleaned_data.get('email')
        user = User.objects.create_user(**user_data)
        return user


class EditUserForm(UserFormMixin, forms.ModelForm):
    """Edit User form"""

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active'
        ]

    def __init__(self, *args, **kwargs):
        """init method for edit user form"""
        self.request = kwargs.pop('request', None)
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = _(settings.VEGA_OPTIONAL_TXT)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'edit-user-form'
        self.helper.layout = Layout(
            Field('first_name'),
            Field('last_name'),
            Field('username'),
            Field('email'),
            Field('is_active'),
            get_form_actions(
                cancel_url=self.vega_extra_kwargs.get("cancel_url", "/")),
        )

    def validate_unique_email(self, value):
        """Validate unique email when editting users"""
        try:
            return get_adapter().validate_unique_email(
                value, user=self.instance)
        except NameError:
            return value
