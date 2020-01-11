"""module for crispy form utils."""
from typing import List

from django.conf import settings
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Div, Layout, Submit


def get_form_actions(  # pylint: disable=bad-continuation
    cancel_url: str,
    submit_text: str = settings.VEGA_SUBMIT_TEXT,
    cancel_text: str = settings.VEGA_CANCEL_TEXT,
) -> FormActions:
    """
    Return the FormActions class.

    :param cancel_url: the cancel url
    :param submit_text: the text for the submit button
    :param cancel_text: the text for the cancel button

    :return: form actions object

    """
    return FormActions(
        Div(
            Div(
                Div(
                    HTML(
                        f"""
                        <a href="{cancel_url}"
                        class="btn btn-default btn-block vega-cancel">
                        {_(cancel_text)}
                        </a>"""
                    ),
                    css_class="col-md-6",
                ),
                Div(
                    Submit("submit", _(submit_text), css_class="btn-block vega-submit"),
                    css_class="col-md-6",
                ),
                css_class="col-md-12",
            ),
            css_class="row",
        )
    )


def get_form_helper_class(  # pylint: disable=too-many-arguments,bad-continuation
    form_tag: bool = True,
    form_method: str = "POST",
    render_required_fields: bool = True,
    form_show_labels: bool = True,
    html5_required: bool = True,
    include_media: bool = True,
) -> FormHelper:
    """
    Return the base form helper class.

    :param form_tag: include form tag?
    :param form_method: form method
    :param render_required_fields: render required fields?
    :param form_show_labels: show form labels?
    :param html5_required: HTML5 required?
    :param include_media: include form media?

    :return: form helper class
    """
    helper = FormHelper()
    helper.form_tag = form_tag
    helper.form_method = form_method
    helper.render_required_fields = render_required_fields
    helper.form_show_labels = form_show_labels
    helper.html5_required = html5_required
    helper.include_media = include_media

    return helper


def get_layout(  # pylint: disable=bad-continuation
    formfields: List[str], with_actions: bool = False, cancel_url: str = "/"
) -> Layout:
    """Get layout class for crispy form helper.

    Arguments:
        formfields {List[str]} -- list of form fields

    Keyword Arguments:
        with_actions {bool} -- whether to include form actions (default: {False})
        cancel_url {str} -- the cancel url (default: {"/"})

    Returns:
        Layout -- the crispy forms Layout object

    """
    layout = Layout(*formfields)
    if with_actions is True:
        form_actions_class = get_form_actions(cancel_url=cancel_url)
        layout.append(form_actions_class)
    return layout
