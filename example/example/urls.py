"""example URL Configuration"""
from django.conf.urls import include
from django.urls import path

from artists import views


urlpatterns = [
    path('', include('vega_admin.contrib.users.urls')),
] + views.ArtistCRUD().url_patterns() +\
    views.SongCRUD().url_patterns()
