"""Tables module"""
import django_tables2 as tables

from .models import Artist


class ArtistTable(tables.Table):
    """
    Artist table class
    """
    class Meta:
        model = Artist
