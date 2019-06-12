"""
Module for vega-admin test models
"""
from django.db import models


class Artist(models.Model):
    """
    Artist Model class
    """

    name = models.CharField(max_length=100)

    class Meta:
        ordering = ["name"]
        verbose_name = "professional artist"
        verbose_name_plural = "professional artists"

    def __str__(self):
        """Unicode representation of Song."""
        return self.name


class Song(models.Model):
    """Model definition for Song."""

    SINGLE = "1"
    COLLABO = "2"
    SKIT = "3"

    SONG_TYPES = ((SINGLE, "Single"), (COLLABO, "Collaboration"), (SKIT, "Skit"))

    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    song_type = models.CharField(
        "Type", max_length=1, choices=SONG_TYPES, default=SINGLE
    )
    release_date = models.DateField("Release Date")
    release_time = models.TimeField("Release Time")
    recording_time = models.DateTimeField("Recording Time", auto_now_add=False)

    class Meta:
        """Meta definition for Song."""

        verbose_name = "Song"
        verbose_name_plural = "Songs"
        ordering = ["name"]

    def __str__(self):
        """Unicode representation of Song."""
        return self.name
