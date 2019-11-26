"""
Module for vega-admin test views
"""
from typing import List, Union

from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django_filters import FilterSet

from vega_admin.mixins import SimpleURLPatternMixin
from vega_admin.views import (
    VegaCreateView,
    VegaCRUDView,
    VegaDeleteView,
    VegaDetailView,
    VegaListView,
    VegaUpdateView,
)

from .forms import (
    ArtistForm,
    CustomSearchForm,
    PlainArtistForm,
    SongForm,
    UpdateArtistForm,
)
from .models import Artist, Song
from .tables import ArtistTable


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


class ArtistRead(VegaDetailView):  # pylint: disable=too-many-ancestors
    """
    Artist detail view
    """

    model = Artist


class ArtistListView(VegaListView):  # pylint: disable=too-many-ancestors
    """
    Artist list view
    """

    model = Artist
    table_class = ArtistTable
    search_fields = ["name"]


class SongCRUD(VegaCRUDView):
    """
    CRUD view for songs
    """

    model = Song
    protected_actions: Union[None, List[str]] = None
    permissions_actions: Union[None, List[str]] = None
    list_fields = ["name", "artist"]
    read_fields = ["name", "artist"]
    table_attrs = {"class": "song-table"}
    table_actions = ["create", "update", "delete"]
    create_fields = ["name", "artist"]
    update_fields = ["name"]


class CustomSongCRUD(SongCRUD):
    """
    CRUD view for songs with login protection
    """

    class CustomListView(ArtistListView):  # pylint: disable=too-many-ancestors
        """custom list view"""

    class FooView(SimpleURLPatternMixin, TemplateView):
        """random template view"""

        template_name = "artist_app/empty.html"

    protected_actions = ["create", "update", "delete", "template", "view"]
    permissions_actions: Union[None, List[str]] = None
    crud_path = "private-songs"
    view_classes = {"artists": CustomListView, "template": FooView}
    form_fields = ["name", "artist"]


class PermsSongCRUD(CustomSongCRUD):
    """
    CRUD view for songs with permissions protection
    """

    protected_actions = ["create", "update", "delete", "artists", "list", "view"]
    permissions_actions = ["create", "update", "delete", "artists", "view"]
    crud_path = "hidden-songs"
    form_class = SongForm


class ArtistCRUD(VegaCRUDView):
    """
    CRUD view for artists
    """

    model = Artist
    protected_actions = None
    permissions_actions = None


class CustomDefaultActions(ArtistCRUD):
    """CRUD view with custom default actions"""

    # pylint: disable=too-many-ancestors
    class CustomCreateView(ArtistCreate):
        """custom Create view"""

    class CustomUpdateView(ArtistUpdate):
        """custom Update view"""

    class CustomListView(ArtistListView):
        """custom list view"""

    class CustomDeleteView(ArtistDelete):
        """custom Delete view"""

    class CustomReadView(ArtistRead):
        """custom Read view"""

    view_classes = {
        "list": CustomListView,
        "view": CustomReadView,
        "update": CustomUpdateView,
        "create": CustomCreateView,
        "delete": CustomDeleteView,
    }
    crud_path = "custom-default-actions"


class BrokenCRUD(VegaCRUDView):
    """CRUD view with broken urls"""

    # pylint: disable=too-many-ancestors
    class BrokenListView(LoginRequiredMixin, VegaListView):
        """View that is broken"""

        model = Artist

    model = Artist
    actions = ["break"]
    permissions_actions = actions
    view_classes = {"break": BrokenListView}
    crud_path = "broken"


class Artist42CRUD(VegaCRUDView):
    """
    CRUD View that sets permission required for custom view class and action
    """

    # pylint: disable=too-many-ancestors
    class CustListView(PermissionRequiredMixin, VegaListView):
        """
        Custom list view that has PermissionRequiredMixin
        """

        model = Artist

    class FooView(SimpleURLPatternMixin, TemplateView):
        """random template view"""

        template_name = "artist_app/empty.html"

    model = Artist
    actions = ["list", "other"]
    permissions_actions = actions
    view_classes = {"list": CustListView, "other": FooView}
    crud_path = "42"


class CustomArtistCRUD(VegaCRUDView):
    """
    CRUD view for artists with custom forms and table
    """

    model = Artist
    protected_actions = None
    permissions_actions = None
    crud_path = "custom-artist"
    form_class = PlainArtistForm
    create_form_class = ArtistForm
    update_form_class = UpdateArtistForm
    table_class = ArtistTable
    search_fields = ["name"]
    search_form_class = CustomSearchForm
    paginate_by = 10


class FilterSongCRUD(VegaCRUDView):
    """
    CRUD view for songs with filtering
    """

    model = Song
    actions = ["list"]
    filter_fields = ["name", "artist"]
    crud_path = "filters"
    search_form_class = None


class Filter2SongCRUD(VegaCRUDView):
    """
    CRUD view for songs with filtering
    """

    class SongFilter(FilterSet):
        """Song filter class"""

        class Meta:
            model = Song
            fields = ["artist"]

    model = Song
    actions = ["list"]
    search_fields = ["artist__name"]
    filter_class = SongFilter
    crud_path = "filters2"
    search_form_class = None


class PlainFormCRUD(VegaCRUDView):
    """Vega CRUD view created with plain form"""

    model = Artist
    permissions_actions = None
    form_class = PlainArtistForm
    actions = ["create", "update", "list"]
    crud_path = "plain-form"
