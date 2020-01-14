"""Module for vega-admin test urls."""
from . import views

urlpatterns = views.BandCRUD().url_patterns()
