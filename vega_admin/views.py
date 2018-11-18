"""
Views module
"""
from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from braces.views import FormMessagesMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from vega_admin.mixins import (DeleteViewMixin, ListViewSearchMixin,
                               PageTitleMixin, VegaFormMixin, VerboseNameMixin)


# pylint: disable=too-many-ancestors
class VegaListView(VerboseNameMixin, ListViewSearchMixin, PageTitleMixin,
                   ExportMixin, SingleTableView, ListView):
    """
    vega-admin Generic List View
    """
    template_name = "vega_admin/basic/list.html"


class VegaCreateView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     VegaFormMixin, CreateView):
    """
    vega-admin Generic Create View
    """
    template_name = "vega_admin/basic/create.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_CREATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaUpdateView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     VegaFormMixin, UpdateView):
    """
    vega-admin Generic Update View
    """
    template_name = "vega_admin/basic/update.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_UPDATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaDeleteView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     DeleteViewMixin, DeleteView):
    """
    vega-admin Generic Delete View
    """
    template_name = "vega_admin/basic/delete.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_DELETE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)
