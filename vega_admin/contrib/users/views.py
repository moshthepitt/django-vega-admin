"""Views module for Vega Admin users app"""
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.urls import reverse_lazy

from vega_admin.contrib.users.forms import (AddUserForm, EditUserForm,
                                            PasswordChangeForm)
from vega_admin.views import VegaCRUDView, VegaUpdateView


class ChangePassword(VegaUpdateView):  # pylint: disable=too-many-ancestors
    """
    Change Password view
    """

    form_class = PasswordChangeForm
    model = User

    def get_success_url(self):  # pylint: disable=no-self-use
        """Get success_url"""
        return reverse_lazy("auth.user-list")


class UserCRUD(VegaCRUDView):
    """
    CRUD view for users
    """

    model = User
    list_fields = ["id", "username", "email", "first_name", "last_name"]
    create_form_class = AddUserForm
    update_form_class = EditUserForm
    protected_actions = None
    permissions_actions = None
    view_classes = {settings.VEGA_CHANGE_PASSWORD_LABEL: ChangePassword}
    table_actions = [
        settings.VEGA_READ_ACTION,
        settings.VEGA_UPDATE_ACTION,
        settings.VEGA_CHANGE_PASSWORD_LABEL,
        settings.VEGA_DELETE_ACTION,
    ]
    order_by = ["-last_login", "first_name"]


class GroupCRUD(VegaCRUDView):
    """
    CRUD view for Groups
    """

    model = Group
    protected_actions = None
    permissions_actions = None
    list_fields = ["id", "name"]
