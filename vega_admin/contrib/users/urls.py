"""example URL Configuration"""
from vega_admin.contrib.users.views import UserCRUD, GroupCRUD

# pylint: disable=invalid-name
urlpatterns = UserCRUD().url_patterns() + GroupCRUD().url_patterns()
