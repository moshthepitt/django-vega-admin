"""
Module for vega-admin test views
"""
from vega_admin.views import (VegaCreateView, VegaDeleteView, VegaListView,
                              VegaUpdateView, VegaCRUDView)

from .forms import ArtistForm
from .models import Artist
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
    search_fields = ['name']
