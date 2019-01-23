"""
vega-admin forms module
"""
from django import forms
from django.conf import settings
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.html import format_html
from django.utils.translation import ugettext as _

import django_tables2 as tables
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit
from django_filters import FilterSet

from vega_admin.mixins import VegaFormMixin


def get_form_actions(cancel_url: str):
    """
    Returns the FormActions class, for use in model forms in VegaCRUD
    """
    return FormActions(
        Div(
            Div(
                Div(
                    HTML(
                        f"""
                        <a href="{cancel_url}"
                        class="btn btn-default btn-block vega-cancel">
                        {_(settings.VEGA_CANCEL_TEXT)}
                        </a>"""
                    ),
                    css_class="col-md-6",
                ),
                Div(
                    Submit(
                        "submit",
                        _(settings.VEGA_SUBMIT_TEXT),
                        css_class="btn-block vega-submit"
                    ),
                    css_class="col-md-6",
                ),
                css_class="col-md-12",
            ),
            css_class="row",
        )
    )


def get_modelform(
        model: object, fields: list = None, extra_fields: list = None):
    """
    Get the a ModelForm for the provided model

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
        self.vega_extra_kwargs = kwargs.pop("vega_extra_kwargs", dict())
        cancel_url = self.vega_extra_kwargs.get("cancel_url", "/")
        form_actions_class = get_form_actions(cancel_url=cancel_url)
        super(modelform_class, self).__init__(*args, **kwargs)
        # add crispy forms FormHelper
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_method = "post"
        self.helper.render_required_fields = True
        self.helper.form_show_labels = True
        self.helper.html5_required = True
        self.helper.include_media = False
        self.helper.form_id = f"{self.model._meta.model_name}-form"
        self.helper.layout = Layout(*self.fields.keys())
        self.helper.layout.append(form_actions_class)

    if fields is None:
        fields = [_.name for _ in model._meta.concrete_fields]

    # the Meta class
    meta_class = type(
        "Meta",  # name of class
        (),  # inherit from object
        {
            "model": model,
            "fields": fields,
        },
    )

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


def get_listview_form(
        model: object, fields: list, include_search: bool = True):
    """
    Get a search and filter form for use in ListViews

    This is essentially a model form with an additional field named `q`.

    :param model: the model class
    :param fields: list of the fields that you want included in the form
    :return: model form
    """
    search_field = None
    if include_search:
        search_field = (
            "q",
            forms.CharField(
                label=_(settings.VEGA_LISTVIEW_SEARCH_QUERY_TXT),
                required=False,)
        )

    if search_field:
        extra_fields = [search_field]
    else:
        extra_fields = None

    return get_modelform(
        model=model, fields=fields, extra_fields=extra_fields)


def get_table(
        model: object, fields: list = None, actions: list = None,
        attrs: dict = None):
    """
    Get the Table Class for the provided model

    :param model: the model class
    :param fields: list of the fields that you want included in the table
    :param actions: list of tuples representing actions and action url names
    :param options: dict representing kwargs/options to pass to the table
    :return: table
    """
    # the Meta class
    meta_options = {
        "model": model,
        "empty_text": _(settings.VEGA_NOTHING_TO_SHOW)}

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
    options = {"Meta": meta_class}

    if isinstance(actions, list):
        # pylint: disable=unused-argument
        def render_actions_fn(self, *args, **kwargs):
            """Render the actions column"""
            record = kwargs['record']
            actions_links = []
            for item in self.actions_list:
                try:
                    url = reverse(item[1])
                except NoReverseMatch:
                    url = reverse(item[1], args=[record.pk])
                name = item[0]
                actions_links.append(
                    f"<a href='{url}' class='vega-action'>{name}</a>")
            actions_links_html = settings.VEGA_ACTION_LINK_SEPARATOR.join(
                actions_links)
            return format_html(actions_links_html)

        options["actions_list"] = actions
        options["action"] = tables.Column(
            verbose_name=_(settings.VEGA_ACTION_COLUMN_NAME),
            accessor=settings.VEGA_ACTION_COLUMN_ACCESSOR_FIELD,
            orderable=False)
        options["render_action"] = render_actions_fn

    # create the table dynamically using type
    table_class = type(
        f"{model.__name__.title()}{settings.VEGA_TABLE_LABEL}",
        (tables.Table, ),
        options,
    )

    return table_class


def get_filterclass(model: object, fields: list = None):
    """
    Get the Filter Class for the provided model

    :param model: the model class
    :param fields: list of the fields that you want included in the table
    :return: filter class
    """
    # the Meta class
    meta_options = {
        "model": model,
        "fields": fields,
    }
    meta_class = type("Meta", (), meta_options)

    # the attributes of our new table class
    options = {"Meta": meta_class}

    # create the filter_class dynamically using type
    filter_class = type(
        f"{model.__name__.title()}{settings.VEGA_FILTER_LABEL}",
        (FilterSet, ),
        options,
    )

    return filter_class
