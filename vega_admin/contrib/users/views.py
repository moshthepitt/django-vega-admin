"""Views module for Vega Admin users app"""
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.urls import reverse_lazy

from vega_admin.contrib.users.forms import (AddUserForm, PasswordChangeForm,
                                            EditUserForm)
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
    list_fields = ['id', 'username', 'email', 'first_name', 'last_name']
    create_form_class = AddUserForm
    update_form_class = EditUserForm
    protected_actions = None
    permissions_actions = None
    view_classes = {
        "change password": ChangePassword,
    }
    table_actions = [
        settings.VEGA_READ_ACTION,
        settings.VEGA_UPDATE_ACTION,
        "change password",
        settings.VEGA_DELETE_ACTION,
    ]


class GroupCRUD(VegaCRUDView):
    """
    CRUD view for Groups
    """

    model = Group
    protected_actions = None
    permissions_actions = None
    # list_fields = ['id', 'name']
