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
    list_fields = ["name", "artist", "release_date"]
    read_fields = [
        "name", "artist", "release_date", "release_time", "recording_time"]
    table_attrs = {"class": "table song-table"}
    table_actions = ["create", "artists", "update", "delete", "view"]
    create_fields = ["name", "artist", "release_date", "release_time"]
    update_fields = ["name", "release_date", "release_time"]
    view_classes = {
        "artists": CustomListView,
    }
