"""
vega-admin mixins module
"""
from django.conf import settings
from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
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
        kwargs['request'] = self.request
        return kwargs


# pylint: disable=too-few-public-methods
class VegaFormMixin(VegaFormKwargsMixin):
    """
    Adds some nice stuff to formviews used in create/update/delete views
    """

    pass


class ListViewSearchMixin:
    """
    Adds search to listview
    """
    form_class = ListViewSearchForm
    search_fields = []
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

        if self.request.GET.get('q'):
            form = self.form_class(self.request.GET)
            if form.is_valid() and self.search_fields:
                search_terms = [
                    "{}__icontains".format(x) for x in self.search_fields
                ]
                query = Q()
                for term in search_terms:
                    query.add(Q(**{term: form.cleaned_data['q']}), Q.OR)
                queryset = queryset.filter(query)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """
        Get context data
        """
        context = super().get_context_data(**kwargs)
        if self.search_fields:
            form = self.form_class(request=self.request)
            if self.request.GET.get('q'):
                form = self.form_class(
                    initial={'q': self.request.GET.get('q')})
            context['vega_listview_search_form'] = form
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
        context['vega_verbose_name'] = self.model._meta.verbose_name
        context['vega_verbose_name_plural'] =\
            self.model._meta.verbose_name_plural
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
        context['vega_page_title'] = getattr(self, 'page_title', None)
        return context


class DeleteViewMixin:
    """
    Mixin for delete views that adds in missing elements
    """
    delete_url = "/"

    def get_delete_url(self):
        """
        Get the delete url for the object in question
        """
        return self.delete_url

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
    def derive_url_pattern(cls, crud_path, action):
        """
        Derive the url pattern
        """
        return f"{crud_path}/{action}/"


class ObjectURLPatternMixin:
    """
    Implements the derive_url_pattern method for single object views
    """

    @classmethod
    def derive_url_pattern(cls, crud_path, action):
        """
        Derive the url pattern
        """
        return f"{crud_path}/{action}/<int:pk>/"
