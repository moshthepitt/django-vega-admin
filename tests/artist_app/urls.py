"""
Module for vega-admin test urls
"""
from django.urls import path

from . import views

urlpatterns = [
    path('edit/artists/create/', views.ArtistCreate.as_view()),
    path('edit/artists/edit/<int:pk>', views.ArtistUpdate.as_view()),
    path('edit/artists/delete/<int:pk>', views.ArtistDelete.as_view()),
]
