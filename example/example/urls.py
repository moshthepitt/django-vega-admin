"""example URL Configuration"""
from artists import views

urlpatterns = views.ArtistCRUD().url_patterns() +\
    views.SongCRUD().url_patterns()
