"""
Module for vega-admin test urls
"""
from django.urls import path

from . import views

artist_crud_patterns = views.ArtistCRUD().url_patterns()
custom_artist_crud_patterns = views.CustomArtistCRUD().url_patterns()
song_crud_patterns = views.SongCRUD().url_patterns()

urlpatterns = [
    path('list/artists/', views.ArtistListView.as_view()),
    path('edit/artists/create/', views.ArtistCreate.as_view()),
    path('edit/artists/edit/<int:pk>', views.ArtistUpdate.as_view()),
    path('edit/artists/delete/<int:pk>', views.ArtistDelete.as_view()),
] + artist_crud_patterns + song_crud_patterns + custom_artist_crud_patterns
