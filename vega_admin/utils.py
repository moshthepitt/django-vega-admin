"""
vega-admin forms module
"""
from django import forms
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit

from vega_admin.mixins import VegaFormMixin


def get_modelform(model: object):
    """
    Get the a ModelForm for the provided model

    :param model:  the model class
    """

    # this is going to be our custom init method
    def _constructor(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.vega_extra_kwargs = kwargs.pop('vega_extra_kwargs', dict())
        cancel_url = self.vega_extra_kwargs['cancel_url']
        super(modelform_class, self).__init__(*args, **kwargs)
        # add crispy forms FormHelper
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'post'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = f'{self.model._meta.model_name}-form'
        self.helper.layout = Layout(*self.fields.keys())
        self.helper.layout.append(
            FormActions(
                Div(Div(
                    Div(HTML(f"""
                                <a href="{cancel_url}"
                                class="btn">
                                Cancel
                                </a>"""),
                        css_class="col-md-6"),
                    Div(Submit('submit', _('Submit'), css_class=''),
                        css_class="col-md-6"),
                    css_class="col-md-12"),
                    css_class="row"), ))

    # the Meta class
    meta_class = type(
        'Meta',  # name of class
        (),  # inherit from object
        {
            'model': model,
            'fields': [_.name for _ in model._meta.concrete_fields]
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
