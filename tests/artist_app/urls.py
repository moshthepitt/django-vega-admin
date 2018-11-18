"""
Module for vega-admin test urls
"""
from django.urls import path

from . import views

urlpatterns = [
    path('edit/artists/create/', views.ArtistCreate.as_view()),
]