"""
vega-admin forms module
"""
from django import forms

from vega_admin.mixins import VegaFormMixin


def get_modelform(model: object):
    """
    Get the a ModelForm for the provided model

    :param model:  the model class
    """
    # this is going to be our custom init method
    def _constructor(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(modelform_class, self).__init__(*args, **kwargs)

    # the Meta class
    meta_class = type(
        'Meta',  # name of class
        (),  # inherit from object
        {
            'model': model,
            'fields': [
                _.name for _ in model._meta.concrete_fields
            ]
        })

    # the attributes of our new modelform
    options = {
        "model": model,
        "__init__": _constructor,
        "Meta": meta_class,
    }

    # create the modelform dynamically using type
    modelform_class = type(
        f'{model.__name__.title()}Form',  # the name of the new model form
        (VegaFormMixin, forms.ModelForm),  # the classes that we should inherit
        options)

    return modelform_class
