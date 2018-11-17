"""
Apps module for django-vega-admin
"""
from django.apps import AppConfig


class VegaAdminConfig(AppConfig):
    """
    Apps config class
    """
    name = 'vega_admin'
    app_label = 'vega_admin'

    def ready(self):
        """
        Do stuff when the app is ready
        """
        # set up app settings
        from django.conf import settings
        import vega_admin.settings as defaults
        for name in dir(defaults):
            if name.isupper() and not hasattr(settings, name):
                setattr(settings, name, getattr(defaults, name))
