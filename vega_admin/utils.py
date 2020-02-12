"""vega-admin forms module."""
from typing import Any, Dict, List, Optional, Tuple, Union

from django import forms
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import DateField, DateTimeField, Model, TimeField
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from django.utils.module_loading import import_string
from django.utils.translation import ugettext as _

import django_tables2 as tables
from django_filters import FilterSet

from vega_admin.crispy_utils import get_default_formhelper, get_layout
from vega_admin.mixins import VegaFormMixin


def get_datefields(model: Model) -> List[str]:
    """
    Get the date fields from a model.

    :param model: the model class
    :return: list of datefield names
    """
    return [
        _.name
        for _ in model._meta.concrete_fields
        if isinstance(_, DateField) and not isinstance(_, DateTimeField)
    ]


def get_datetimefields(model: Model) -> List[str]:
    """
    Get the datetime fields from a model.

    :param model: the model class
    :return: list of datetimefield names
    """
    return [_.name for _ in model._meta.concrete_fields if isinstance(_, DateTimeField)]


def get_timefields(model: Model) -> List[str]:
    """
    Get the time fields from a model.

    :param model: the model class
    :return: list of timefield names
    """
    return [_.name for _ in model._meta.concrete_fields if isinstance(_, TimeField)]


def get_modelform(model: Model, fields: list = None, extra_fields: list = None):
    """
    Get the ModelForm for the provided model.

    :param model: the model class
    :param fields: list of the fields that you want included in the form
    :param extra_fields: extra fields that you want included in the form
    :return: model form

    extra_fields needs to be a list of tuples, like so:

    extra_fields = [("q", forms.CharField(
            label=_(settings.VEGA_LISTVIEW_SEARCH_QUERY_TXT),
            required=False,))]
    """
    # this is going to be our custom init method
    def _constructor(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        self.vega_extra_kwargs = kwargs.pop(settings.VEGA_MODELFORM_KWARG, dict())
        super(modelform_class, self).__init__(*args, **kwargs)
        # add crispy forms FormHelper
        self.helper = get_default_formhelper()
        self.helper.form_id = f"{self.model._meta.model_name}-form"
        self.helper.layout = get_layout(
            self.fields.keys(),
            with_actions=True,
            cancel_url=self.vega_extra_kwargs.get("cancel_url", "/"),
        )

    if fields is None:
        fields = [field.name for field in model._meta.get_fields() if field.editable]

    widgets = {}
    # set the widgets for all date input fields
    for datefield in get_datefields(model):
        widgets[datefield] = import_string(settings.VEGA_DATE_WIDGET)

    # set the widgets for all datetime input fields
    for datetimefield in get_datetimefields(model):
        widgets[datetimefield] = import_string(settings.VEGA_DATETIME_WIDGET)

    # set the widgets for all time input fields
    for timefield in get_timefields(model):
        widgets[timefield] = import_string(settings.VEGA_TIME_WIDGET)

    meta_class_options = {"model": model, "fields": fields}

    if widgets:
        meta_class_options["widgets"] = widgets

    # the Meta class
    meta_class = type("Meta", (), meta_class_options)

    # the attributes of our new modelform
    options = {"model": model, "__init__": _constructor, "Meta": meta_class}

    # add extra fields
    if extra_fields:
        for extra_field in extra_fields:
            options[extra_field[0]] = extra_field[1]

    # create the modelform dynamically using type
    modelform_class = type(
        f"{model.__name__.title()}{settings.VEGA_FORM_LABEL}",
        (VegaFormMixin, forms.ModelForm),
        options,
    )

    return modelform_class


def get_listview_form(model: Model, fields: List[str], include_search: bool = True):
    """
    Get a search and filter form for use in ListViews.

    This is essentially a model form with an additional field named `q`.

    :param model: the model class
    :param fields: list of the fields that you want included in the form
    :return: model form
    """
    search_field: Optional[Tuple[str, Any]] = None
    if include_search:
        search_field = (
            "q",
            forms.CharField(
                label=_(settings.VEGA_LISTVIEW_SEARCH_QUERY_TXT), required=False
            ),
        )

    extra_fields: Optional[List[Tuple[str, Any]]] = None
    if search_field:
        extra_fields = [search_field]

    return get_modelform(model=model, fields=fields, extra_fields=extra_fields)


def get_table(  # pylint: disable=bad-continuation
    model: Model,
    fields: Optional[List[str]] = None,
    actions: Optional[List[str]] = None,
    attrs: Optional[dict] = None,
):
    """
    Get the Table Class for the provided model.

    :param model: the model class
    :param fields: list of the fields that you want included in the table
    :param actions: list of tuples representing actions and action url names
    :param options: dict representing kwargs/options to pass to the table
    :return: table
    """
    # the Meta class
    meta_options = {"model": model, "empty_text": _(settings.VEGA_NOTHING_TO_SHOW)}

    if fields:
        all_fields = [_.name for _ in model._meta.concrete_fields]
        exclude_fields = [_ for _ in all_fields if _ not in fields]
        # get sequence
        sequence_list = fields
        if "..." not in sequence_list:
            sequence_list.append("...")
        # set meta options
        meta_options["exclude"] = exclude_fields
        meta_options["sequence"] = tuple(sequence_list)

    if attrs:
        meta_options["attrs"] = attrs

    meta_class = type("Meta", (), meta_options)

    # the attributes of our new table class
    options: Dict[Any, Any] = {"Meta": meta_class}

    if isinstance(actions, list):
        # pylint: disable=unused-argument
        def render_actions_fn(self, *args, **kwargs):
            """Render the actions column."""
            record = kwargs["record"]
            actions_links = []
            for item in self.actions_list:
                try:
                    url = reverse(item[1])
                except NoReverseMatch:
                    url = reverse(item[1], args=[record.pk])
                name = item[0]
                actions_links.append(f"<a href='{url}' class='vega-action'>{name}</a>")
            actions_links_html = settings.VEGA_ACTION_LINK_SEPARATOR.join(actions_links)
            return format_html(actions_links_html)

        options["actions_list"] = actions
        options["action"] = tables.Column(
            verbose_name=_(settings.VEGA_ACTION_COLUMN_NAME),
            accessor=settings.VEGA_ACTION_COLUMN_ACCESSOR_FIELD,
            orderable=False,
        )
        options["render_action"] = render_actions_fn

    # create the table dynamically using type
    table_class = type(
        f"{model.__name__.title()}{settings.VEGA_TABLE_LABEL}", (tables.Table,), options
    )

    return table_class


def get_filterclass(model: Model, fields: list = None):
    """
    Get the Filter Class for the provided model.

    :param model: the model class
    :param fields: list of the fields that you want included in the table
    :return: filter class
    """
    # the Meta class
    meta_options = {"model": model, "fields": fields}
    meta_class = type("Meta", (), meta_options)

    # the attributes of our new table class
    options = {"Meta": meta_class}

    # create the filter_class dynamically using type
    filter_class = type(
        f"{model.__name__.title()}{settings.VEGA_FILTER_LABEL}", (FilterSet,), options
    )

    return filter_class


def customize_modelform(form_class: Union[forms.Form, forms.ModelForm]):
    """
    Add custom keyword arguments to a provided form class.

    - Adds the custom kwargs required for vega_admin, if they are missing.
    - Adds a crispy form helper if missing

    Arguments:
        form_class {Union[Form, ModelForm]} -- the form class

    Returns:
        {Union[Form, ModelForm]} -- the customized form class

    """
    # the try here would fail with a TypeError if settings.VEGA_MODELFORM_KWARG
    # is not a valid kwarg
    try:
        form_class(**{settings.VEGA_MODELFORM_KWARG: dict()})
    except ObjectDoesNotExist:
        # we don't care about these exceptions right now because forms that have
        # an instance are likely to end up here as we are not supplying that
        # instance in the try statements
        pass
    except TypeError:
        # pylint: disable=missing-class-docstring,too-few-public-methods,inherit-non-class
        class VegaCustomFormClass(form_class):  # type: ignore
            def __init__(self, *args, **kwargs):
                self.request = kwargs.pop("request", None)
                self.vega_extra_kwargs = kwargs.pop(
                    settings.VEGA_MODELFORM_KWARG, dict()
                )
                super().__init__(*args, **kwargs)
                if not hasattr(self, "helper"):
                    self.helper = get_default_formhelper()
                    self.helper.form_id = f"{self.Meta.model._meta.model_name}-form"
                    self.helper.layout = get_layout(
                        self.fields.keys(),
                        with_actions=True,
                        cancel_url=self.vega_extra_kwargs.get("cancel_url", "/"),
                    )

        return VegaCustomFormClass

    return form_class
