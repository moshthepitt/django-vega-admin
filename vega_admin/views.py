"""
Views module
"""
from braces.views import FormMessagesMixin
from django.conf import settings
from django.urls import path
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from vega_admin.mixins import (DeleteViewMixin, ListViewSearchMixin,
                               ObjectURLPatternMixin, PageTitleMixin,
                               SimpleURLPatternMixin, VegaFormMixin,
                               VerboseNameMixin)


# pylint: disable=too-many-ancestors
class VegaListView(VerboseNameMixin, ListViewSearchMixin, PageTitleMixin,
                   ExportMixin, SingleTableView, SimpleURLPatternMixin,
                   ListView):
    """
    vega-admin Generic List View
    """
    template_name = "vega_admin/basic/list.html"


class VegaCreateView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     VegaFormMixin, SimpleURLPatternMixin, CreateView):
    """
    vega-admin Generic Create View
    """
    template_name = "vega_admin/basic/create.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_CREATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaUpdateView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     VegaFormMixin, ObjectURLPatternMixin, UpdateView):
    """
    vega-admin Generic Update View
    """
    template_name = "vega_admin/basic/update.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_UPDATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaDeleteView(FormMessagesMixin, PageTitleMixin, VerboseNameMixin,
                     DeleteViewMixin, ObjectURLPatternMixin, DeleteView):
    """
    vega-admin Generic Delete View
    """
    template_name = "vega_admin/basic/delete.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_DELETE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaCRUDView(object):
    """
    Creates generic CRUD views for a model automagically

    The intention is for you to give it at least a model and get back an entire
    set of CRUD views, with everyhting you need to start doing CRUD actions
    straight away.
    """
    actions = ['create', 'update', 'list', 'delete']

    def __init__(self, model=None):
        """
        Initialize!
        """
        if model is not None:
            self.model = model
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label
        self.crud_path = self.model._meta.label_lower

    def get_view_classes(self):
        """
        Returns the available views
        """
        return {
            'list': VegaListView,
            'create': VegaCreateView,
            'update': VegaUpdateView,
            'delete': VegaDeleteView,
        }

    def get_view_class_for_action(self, action: str):
        """
        Get the view for an action
        """
        view_classes = self.get_view_classes()
        try:
            ViewClass = view_classes[action]
        except KeyError:
            # this action is not supported
            raise Exception(settings.VEGA_INVALID_ACTION)
        else:
            ViewClass.model = self.model
            return ViewClass

    def get_url_name_for_action(self, action: str):
        """
        Returns the url name for the action
        """
        return f"{self.crud_path}-{action}"

    def get_url_pattern_for_action(self, view_class, action: str):
        """
        Returns the url pattern for the provided action
        """
        try:
            return view_class.derive_url_pattern(self.crud_path, action)
        except NameError:
            # the view does not know how to derive a url pattern
            # we are forced to try something and hope it works :(
            return f"{self.crud_path}/{action}/"

    def url_patterns(self):
        """
        Returns the URL patters for all the actions in this CRUD view
        """
        urls = []
        for action in self.actions:
            ViewClass = self.get_view_class_for_action(action=action)
            pattern = self.get_url_pattern_for_action(ViewClass, action)
            url_name = self.get_url_name_for_action(action=action)
            urls.append(path(pattern, ViewClass.as_view(), name=url_name))
        return urls
