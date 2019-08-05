"""
Module for vega-admin test models
"""
from django.db import models
from django.utils.translation import ugettext as _


class Artist(models.Model):
    """
    Artist Model class
    """

    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "Artist"
        verbose_name_plural = "Artists"

    def __str__(self):
        """Unicode representation of Song."""
        return self.name


class Song(models.Model):
    """Model definition for Song."""

    SINGLE = "1"
    COLLABO = "2"
    SKIT = "3"

    SONG_TYPES = ((SINGLE, "Single"), (COLLABO, "Collaboration"), (SKIT,
                                                                   "Skit"))

    artist = models.ForeignKey(
        Artist, verbose_name=_("Artist"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=100)
    song_type = models.CharField(
        _("Type"), max_length=1, choices=SONG_TYPES, default=SINGLE)
    release_date = models.DateField(_("Release Date"))
    release_time = models.TimeField(_("Release Time"))
    recording_time = models.DateTimeField(
        _("Recording Time"), auto_now_add=True)

    class Meta:
        """Meta definition for Song."""

        verbose_name = "Song"
        verbose_name_plural = "Songs"
        ordering = ["name"]

    def __str__(self):
        """Unicode representation of Song."""
        return self.name
