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
        ordering = ['name']
        verbose_name = 'professional artist'
        verbose_name_plural = 'professional artists'

    def __str__(self):
        """Unicode representation of Song."""
        return self.name


class Song(models.Model):
    """Model definition for Song."""
    artist = models.ForeignKey(Artist, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Song."""
        verbose_name = 'Song'
        verbose_name_plural = 'Songs'
        ordering = ['name']

    def __str__(self):
        """Unicode representation of Song."""
        return self.name
