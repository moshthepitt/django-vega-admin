"""Views module for Vega Admin users app"""
from vega_admin.views import VegaCRUDView
from django.contrib.auth.models import User
from vega_admin.contrib.users.forms import AddUserForm, EditUserForm


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
