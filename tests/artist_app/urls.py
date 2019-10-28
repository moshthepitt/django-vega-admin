"""
Module for vega-admin test urls
"""
from django.urls import path

from . import views

# pylint: disable=invalid-name
artist_crud_patterns = views.ArtistCRUD().url_patterns()
custom_artist_crud_patterns = views.CustomArtistCRUD().url_patterns()
song_crud_patterns = views.SongCRUD().url_patterns()
protected_crud_song_patterns = views.CustomSongCRUD().url_patterns()
perms_crud_song_patterns = views.PermsSongCRUD().url_patterns()
custom_default_patterns = views.CustomDefaultActions().url_patterns()
patterns_42 = views.Artist42CRUD().url_patterns()
plainform_patterns = views.PlainFormCRUD().url_patterns()


urlpatterns = (
    [
        path("list/artists/", views.ArtistListView.as_view()),
        path("edit/artists/create/", views.ArtistCreate.as_view()),
        path("view/artists/view/<int:pk>", views.ArtistRead.as_view()),
        path("edit/artists/edit/<int:pk>", views.ArtistUpdate.as_view()),
        path("edit/artists/delete/<int:pk>", views.ArtistDelete.as_view()),
    ]
    + artist_crud_patterns
    + song_crud_patterns
    + custom_artist_crud_patterns
    + protected_crud_song_patterns
    + custom_default_patterns
    + perms_crud_song_patterns
    + patterns_42
    + plainform_patterns
)
