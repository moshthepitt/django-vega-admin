"""Artist app views module"""
from vega_admin.views import VegaCRUDView, VegaListView

from .models import Artist, Song


class ArtistCRUD(VegaCRUDView):
    """
    CRUD view for artists
    """

    model = Artist
    protected_actions = None
    permissions_actions = None


class SongCRUD(VegaCRUDView):
    """
    CRUD view for songs
    """

    class CustomListView(VegaListView):
        """Custom list view"""
        model = Artist

    model = Song
    protected_actions = None
    permissions_actions = None
    list_fields = ["name", "artist", ]
    read_fields = ["name", "artist", ]
    table_attrs = {"class": "table song-table"}
    table_actions = ["create", "artists", "update", "delete", ]
    create_fields = ["name", "artist", ]
    update_fields = ["name", ]
    view_classes = {
        "artists": CustomListView,
    }
