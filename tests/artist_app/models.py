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
        return self.name
