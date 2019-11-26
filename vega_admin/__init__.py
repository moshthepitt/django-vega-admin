"""
Main init file for vega_admin
"""
VERSION = (0, 0, 16)
__version__ = ".".join(str(v) for v in VERSION)
# pylint: disable=invalid-name
default_app_config = "vega_admin.apps.VegaAdminConfig"  # noqa
