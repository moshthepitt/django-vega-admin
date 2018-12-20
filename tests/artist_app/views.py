"""
Module for vega-admin test views
"""
from vega_admin.views import (VegaCreateView, VegaCRUDView, VegaDeleteView,
                              VegaListView, VegaUpdateView)

from .forms import ArtistForm
from .models import Artist, Song
from .tables import ArtistTable


class ArtistCRUD(VegaCRUDView):
    """
    CRUD view for artists
    """

    model = Artist


class ArtistCreate(VegaCreateView):  # pylint: disable=too-many-ancestors
    """
    Artist CreateView class
    """

    form_class = ArtistForm
    model = Artist

    def get_success_url(self):
        """
        Method to get success url
        """
        return "/edit/artists/create/"


class ArtistUpdate(VegaUpdateView):  # pylint: disable=too-many-ancestors
    """
    Artist UpdateView class
    """

    form_class = ArtistForm
    model = Artist

    def get_success_url(self):
        """
        Method to get success url
        """
        return f"/edit/artists/edit/{self.object.id}"


class ArtistDelete(VegaDeleteView):  # pylint: disable=too-many-ancestors
    """
    Artist DeleteView class
    """

    model = Artist

    def get_success_url(self):
        """
        Method to get success url
        """
        return "/edit/artists/create/"


class ArtistListView(VegaListView):  # pylint: disable=too-many-ancestors
    """
    Artist list view
    """

    model = Artist
    table_class = ArtistTable
    search_fields = ["name"]


class SongCRUD(VegaCRUDView):
    """
    CRUD view for artists
    """

    model = Song
    list_fields = ["name", "artist"]
    table_attrs = {"class": "song-table"}
    table_actions = ["create", "update", "list", "delete"]
