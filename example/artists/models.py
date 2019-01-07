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
        ordering = ['name']
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

    def __str__(self):
        """Unicode representation of Song."""
        return self.name


class Song(models.Model):
    """Model definition for Song."""
    artist = models.ForeignKey(
        Artist, verbose_name=_("Artist"), on_delete=models.PROTECT)
    name = models.CharField(_("Name"), max_length=100)

    class Meta:
        """Meta definition for Song."""
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'
        ordering = ['name']

    def __str__(self):
        """Unicode representation of Song."""
        return self.name
