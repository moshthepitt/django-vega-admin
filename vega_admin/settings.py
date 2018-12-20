"""
vega-admin settings module
"""
from django.conf import settings

# crispy forms
VEGA_CRISPY_TEMPLATE_PACK = getattr(
    settings, "CRISPY_TEMPLATE_PACK", "bootstrap3")

# strings
VEGA_FORM_VALID_CREATE_TXT = "Created successfully!"
VEGA_FORM_VALID_UPDATE_TXT = "Updated successfully!"
VEGA_FORM_VALID_DELETE_TXT = "Deleted successfully!"
VEGA_FORM_INVALID_TXT = "Please correct the errors on the form."
VEGA_DELETE_PROTECTED_ERROR_TXT = (
    "You cannot delete this item, it is referenced by other items."
)
VEGA_LISTVIEW_SEARCH_TXT = "Search"
VEGA_LISTVIEW_SEARCH_QUERY_TXT = "Search Query"
VEGA_NOTHING_TO_SHOW = "Nothing to show"
VEGA_CANCEL_TEXT = "Cancel"
VEGA_SUBMIT_TEXT = "Submit"
VEGA_TABLE_LABEL = "Table"
VEGA_FORM_LABEL = "Form"
VEGA_ACTION_COLUMN_NAME = ""
VEGA_ACTION_COLUMN_ACCESSOR_FIELD = "pk"
VEGA_ACTION_LINK_SEPARATOR = " | "

# exceptions
VEGA_INVALID_ACTION = "Invalid Action"
