"""
Module for vega-admin test broken urls
"""
from . import views


urlpatterns = views.BrokenCRUD().url_patterns()
