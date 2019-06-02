"""Widgets module for django-vega-admin"""
from django.forms import DateInput


class VegaDateWidget(DateInput):
    """HTML5 Date input widget class"""
    input_type = 'date'
