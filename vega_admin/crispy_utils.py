"""module for crispy form utils."""
from typing import List

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


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


def get_layout(formfields: List[str]):
    """Get layout class for crispy form helper."""
    return Layout(*formfields)
