"""
vega-admin mixins module
"""
from django.conf import settings
from django.contrib import messages
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.utils.translation import ugettext as _

from vega_admin.forms import ListViewSearchForm


class VegaFormKwargsMixin(object):
    """
    Adds form kwargs
    """

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class VegaFormMixin(VegaFormKwargsMixin):
    """
    Adds some nice stuff to formviews used in create/update/delete views
    """

    pass


class ListViewSearchMixin(object):
    """
    Adds search to listview
    """
    form_class = ListViewSearchForm
    search_fields = []
    filter_class = None

    def get_queryset(self):

        queryset = super().get_queryset()

        if self.filter_class:
            # pylint: disable=not-callable
            f = self.filter_class(self.request.GET, queryset=queryset)
            queryset = f.qs

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
        context = super().get_context_data(**kwargs)
        if self.search_fields:
            form = self.form_class(request=self.request)
            if self.request.GET.get('q'):
                form = self.form_class(
                    initial={'q': self.request.GET.get('q')})
            context['vega_listview_search_form'] = form
        return context


class VerboseNameMixin(object):
    """
    Sets the Model verbose name in the context data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vega_verbose_name'] = self.model._meta.verbose_name
        context['vega_verbose_name_plural'] =\
            self.model._meta.verbose_name_plural
        return context


class PageTitleMixin(object):
    """
    Sets the page title in the context data
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vega_page_title'] = getattr(self, 'page_title', None)
        return context


class DeleteViewMixin(object):
    """
    Mixin for delete views that adds in missing elements
    """
    def delete(self, request, *args, **kwargs):
        # Handle cases where you get ProtectedError
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            info = _(settings.VEGA_DELETE_PROTECTED_ERROR_TXT)
            messages.error(request, info, fail_silently=True)
            return redirect(self.get_delete_url())
