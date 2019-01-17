"""
vega-admin forms module
"""
from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import Field, FieldWithButtons
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from vega_admin.settings import VEGA_LISTVIEW_SEARCH_QUERY_TXT


class ListViewSearchForm(forms.Form):
    """
    search form for use in the vega-admin list view
    """

    q = forms.CharField(
        label=_(
            getattr(settings, 'VEGA_LISTVIEW_SEARCH_QUERY_TXT',
                    VEGA_LISTVIEW_SEARCH_QUERY_TXT)),
        required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = 'GET'
        self.helper.render_required_fields = True
        self.helper.form_show_labels = False
        self.helper.html5_required = True
        self.helper.form_id = 'vega-search-form'
        self.helper.form_class = 'form-inline'
        self.helper.field_template = \
            f'{settings.VEGA_CRISPY_TEMPLATE_PACK}/layout/inline_field.html'
        self.helper.layout = Layout(
            FieldWithButtons(
                Field('q', css_class="input-sm"),
                Submit(
                    'submitBtn',
                    _(settings.VEGA_LISTVIEW_SEARCH_TXT),
                    css_class='btn-sm'
                ),
            )
        )
