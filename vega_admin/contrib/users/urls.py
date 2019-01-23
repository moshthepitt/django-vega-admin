"""example URL Configuration"""
from vega_admin.contrib.users import views

urlpatterns = views.UserCRUD().url_patterns()  # pylint: disable=invalid-name
