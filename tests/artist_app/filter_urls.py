"""
Module for vega-admin test broken urls
"""
from . import views


urlpatterns = views.FilterSongCRUD().url_patterns() +\
              views.Filter2SongCRUD().url_patterns()
