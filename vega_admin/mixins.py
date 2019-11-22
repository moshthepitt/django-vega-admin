"""
vega-admin mixins module
"""
from typing import List

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext as _

from vega_admin.forms import ListViewSearchForm


class VegaFormKwargsMixin:  # pylint: disable=too-few-public-methods
    """
    Adds form kwargs
    """

    def get_form_kwargs(self):
        """
        Adds kwargs to the form
        """
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs


# pylint: disable=too-few-public-methods
class VegaFormMixin(VegaFormKwargsMixin):
    """
    Adds some nice stuff to formviews used in create/update/delete views
    """


class VegaOrderedQuerysetMixin:
    """
    Optionally ensures querysets are ordered
    """

    order_by = None

    def get_order_by(self):
        """Get the field to use when ordering"""
        return self.order_by or settings.VEGA_ORDERING_FIELD

    def get_queryset(self):
        """
        Get the queryset
        """
        queryset = super().get_queryset()
        if not queryset.ordered and settings.VEGA_FORCE_ORDERING:
            order_by = self.get_order_by()
            queryset = queryset.order_by(*order_by)

        return queryset


class ListViewSearchMixin:
    """
    Adds search to listview
    """

    form_class = ListViewSearchForm
    search_fields: List[str] = []
    filter_class = None

    def get_queryset(self):
        """
        Get the queryset
        """
        queryset = super().get_queryset()

        if self.filter_class:
            # pylint: disable=not-callable
            the_filter = self.filter_class(self.request.GET, queryset=queryset)
            queryset = the_filter.qs

        if self.request.GET.get("q"):
            form = self.form_class(self.request.GET)
            if form.is_valid() and self.search_fields:
                search_terms = [f"{x}__icontains" for x in self.search_fields]
                query = Q()
                for term in search_terms:
                    query.add(Q(**{term: form.cleaned_data["q"]}), Q.OR)
                queryset = queryset.filter(query)

        return queryset.distinct()

    def get_search_form_values(self):
        """Get search form values"""
        fields = []
        if self.filter_class:
            for field in self.filter_class.Meta.fields:
                fields.append(field)
        if self.search_fields:
            fields.append("q")
        # build the form values dict
        result = {}
        for item in fields:
            result[item] = self.request.GET.get(item)

        return result

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        if self.search_fields or self.filter_class:
            form = self.form_class(request=self.request)
            initial_values = self.get_search_form_values()
            form = self.form_class(initial=initial_values)
            context["vega_listview_search_form"] = form

        return context


class VerboseNameMixin:
    """
    Sets the Model verbose name in the context data
    """

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        context["vega_verbose_name"] = self.model._meta.verbose_name
        context["vega_verbose_name_plural"] = self.model._meta.verbose_name_plural
        return context


class PageTitleMixin:
    """
    Sets the page title in the context data
    """

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        context["vega_page_title"] = getattr(self, "page_title", None)
        return context


class CRUDURLsMixin:
    """
    Mixin that adds some CRUD helper urls
    """

    cancel_url = "/"
    cancel_url_name = None
    delete_url = "/"
    delete_url_name = None
    read_url = "/"
    read_url_name = None
    list_url = "/"
    list_url_name = None
    create_url = "/"
    create_url_name = None
    update_url = "/"
    update_url_name = None

    def get_crud_url(  # pylint: disable=no-self-use,bad-continuation
        self, url: str, url_name: str, url_kwargs: dict = None
    ):
        """
        Helper function that returns a url

        Attempt to use reverse_lazy to get the url, otherwise return what we
        hope are safe defaults

        :param url: the url
        :param url_name: the url name
        :param url_kwargs: the url kwargs

        :return: url
        """
        if url_name:
            if url_kwargs:
                return reverse_lazy(url_name, kwargs=url_kwargs)
            return reverse_lazy(url_name)
        return url

    def get_create_url(self):
        """
        Get the create url for the object in question

        :return: url
        """
        return self.get_crud_url(url=self.create_url, url_name=self.create_url_name)

    def get_list_url(self):
        """
        Get the cancel url for the object in question

        :return: url
        """
        return self.get_crud_url(url=self.list_url, url_name=self.list_url_name)

    def get_update_url(self):
        """
        Get the update url for the object in question

        :return: url
        """
        return self.get_crud_url(
            url=self.update_url,
            url_name=self.update_url_name,
            url_kwargs={"pk": self.object.pk},
        )

    def get_read_url(self):
        """
        Get the read url for the object in question

        :return: url
        """
        return self.get_crud_url(
            url=self.read_url,
            url_name=self.read_url_name,
            url_kwargs={"pk": self.object.pk},
        )

    def get_delete_url(self):
        """
        Get the delete url for the object in question

        :return: url
        """
        return self.get_crud_url(
            url=self.delete_url,
            url_name=self.delete_url_name,
            url_kwargs={"pk": self.object.pk},
        )

    def get_cancel_url(self):
        """
        Get the cancel url for the object in question

        :return: url
        """
        return self.get_crud_url(url=self.cancel_url, url_name=self.cancel_url_name)

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        context["vega_create_url"] = self.get_create_url()
        context["vega_list_url"] = self.get_list_url()
        context["vega_cancel_url"] = self.get_cancel_url()
        if hasattr(self, "object") and self.object is not None:
            context["vega_read_url"] = self.get_read_url()
            context["vega_delete_url"] = self.get_delete_url()
            context["vega_update_url"] = self.get_update_url()
        return context

    def get_form_kwargs(self):
        """
        Adds kwargs to the form
        """
        kwargs = super().get_form_kwargs()
        url_kwargs = {"cancel_url": self.get_list_url()}
        kwargs[settings.VEGA_MODELFORM_KWARG] = url_kwargs
        return kwargs


class ObjectTitleMixin:
    """Mixin for getting object title"""

    def get_title(self):
        """
        By default we just return the string representation of our object
        """
        return str(self.object)

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        context["vega_object_title"] = self.get_title()
        return context


class DetailViewMixin:
    """Mixin for detail views"""

    fields = None

    def get_fields(self):
        """
        We first default to using our 'fields' variable if available,
        otherwise we figure it out from our object.
        """
        if self.fields and isinstance(self.fields, list):
            return self.fields
        return [_.name for _ in self.object._meta.fields]

    def get_field_value(self, field):
        """Get the value of a field"""
        if field.is_relation:
            try:
                return str(getattr(self.object, field.name))
            except AttributeError:
                return None
        # pylint: disable=protected-access
        return self.object._get_FIELD_display(field)

    def get_object_data(self):
        """Returns a dict of the data in the object"""
        result = {}
        fields_list = self.get_fields()
        for item in fields_list:
            try:
                field = self.object._meta.get_field(item)
            except FieldDoesNotExist:
                pass
            else:
                result[field.verbose_name] = self.get_field_value(field)

        return result

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        context["vega_read_fields"] = self.get_fields()
        context["vega_object_data"] = self.get_object_data()
        return context


class DeleteViewMixin:
    """
    Mixin for delete views that adds in missing elements
    """

    def delete(self, request, *args, **kwargs):
        """
        Custom delete method
        """
        # Handle cases where you get ProtectedError
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            info = _(settings.VEGA_DELETE_PROTECTED_ERROR_TXT)
            messages.error(request, info, fail_silently=True)

            return redirect(self.get_delete_url())


class SimpleURLPatternMixin:
    """
    very simply implements the derive_url_pattern method
    """

    @classmethod
    def derive_url_pattern(cls, crud_path: str, action: str):
        """
        Derive the url pattern
        """
        return f"{crud_path}/{action}/"


class ObjectURLPatternMixin:
    """
    Implements the derive_url_pattern method for single object views
    """

    @classmethod
    def derive_url_pattern(cls, crud_path: str, action: str):
        """
        Derive the url pattern
        """
        return f"{crud_path}/{action}/<int:pk>/"


class TimeStampedModel(models.Model):
    """
    Adds timestamps to a model class
    """

    created = models.DateTimeField(_("Created"), auto_now_add=True)
    modified = models.DateTimeField(_("Modified"), auto_now=True)

    class Meta:
        """Meta class"""

        abstract = True
