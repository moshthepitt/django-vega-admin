"""Widgets module for django-vega-admin"""
from django.forms import DateInput, TimeInput


class VegaDateWidget(DateInput):
    """HTML5 Date input widget class"""
    input_type = 'date'


class VegaTimeWidget(TimeInput):
    """HTML5 Time input widget class"""
    input_type = 'time'
