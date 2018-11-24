"""
Module for vega-admin test views
"""
from vega_admin.views import VegaCreateView, VegaUpdateView, VegaDeleteView
from .models import Artist
from .forms import ArtistForm


class ArtistCreate(VegaCreateView):
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


class ArtistUpdate(VegaUpdateView):
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


class ArtistDelete(VegaDeleteView):
    """
    Artist DeleteView class
    """
    model = Artist

    def get_success_url(self):
        """
        Method to get success url
        """
        return "/edit/artists/create/"
