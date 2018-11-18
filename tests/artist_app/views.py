"""
Module for vega-admin test views
"""
from vega_admin.views import VegaCreateView
from .models import Artist
from .forms import ArtistForm


class ArtistCreate(VegaCreateView):
    """
    Author CreateView class
    """
    form_class = ArtistForm
    model = Artist

    def get_success_url(self):
        """
        Method to get success url
        """
        return "/edit/artists/create/"