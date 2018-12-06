"""
Module for vega-admin test forms
"""
from django import forms

from crispy_forms.bootstrap import Field, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import Artist


class ArtistForm(forms.ModelForm):
    """
    Artist ModelForm class
    """

    class Meta:
        model = Artist
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.vega_extra_kwargs = kwargs.pop('vega_extra_kwargs', dict())
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = 'artist'
        self.helper.layout = Layout(
            Field('name',),
            FormActions(
                Submit('submitBtn',
                       'Submit',
                       css_class='btn-success btn-block'),
            )
        )
