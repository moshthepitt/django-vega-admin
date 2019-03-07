"""AppConfig module for Vega Admin users app"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class UsersConfig(AppConfig):
    """App config class"""

    name = "vega_admin.contrib.users"
    app_label = "vega_admin"
    verbose_name = _("Vega Admin Users")
