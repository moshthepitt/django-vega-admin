"""
vega-admin settings module
"""
from django.conf import settings

# general
VEGA_CREATE_ACTION = "create"
VEGA_READ_ACTION = "view"
VEGA_UPDATE_ACTION = "update"
VEGA_LIST_ACTION = "list"
VEGA_DELETE_ACTION = "delete"
VEGA_DEFAULT_ACTIONS = [
    VEGA_CREATE_ACTION,
    VEGA_READ_ACTION,
    VEGA_UPDATE_ACTION,
    VEGA_LIST_ACTION,
    VEGA_DELETE_ACTION,
]
VEGA_TEMPLATE = "basic"
# ensures that listview queries are ordered
VEGA_FORCE_ORDERING = True
VEGA_ORDERING_FIELD = ["-pk"]

# model forms
VEGA_MODELFORM_KWARG = "vega_extra_kwargs"

# crispy forms
VEGA_CRISPY_TEMPLATE_PACK = getattr(settings, "CRISPY_TEMPLATE_PACK", "bootstrap3")

# strings
VEGA_FORM_VALID_CREATE_TXT = "Created successfully!"
VEGA_FORM_VALID_UPDATE_TXT = "Updated successfully!"
VEGA_FORM_VALID_DELETE_TXT = "Deleted successfully!"
VEGA_FORM_INVALID_TXT = "Please correct the errors on the form."
VEGA_DELETE_PROTECTED_ERROR_TXT = (
    "You cannot delete this item, it is referenced by other items."
)
VEGA_PERMREQUIRED_NOT_SET_TXT = "PermissionRequiredMixin not set for"
VEGA_LISTVIEW_SEARCH_TXT = "Search"
VEGA_LISTVIEW_SEARCH_QUERY_TXT = "Search Query"
VEGA_NOTHING_TO_SHOW = "Nothing to show"
VEGA_CANCEL_TEXT = "Cancel"
VEGA_SUBMIT_TEXT = "Submit"
VEGA_TABLE_LABEL = "Table"
VEGA_FORM_LABEL = "Form"
VEGA_VIEW_LABEL = "View"
VEGA_FILTER_LABEL = "Filter"
VEGA_PROTECTED_LABEL = "Protected"
VEGA_ACTION_COLUMN_NAME = ""
VEGA_ACTION_COLUMN_ACCESSOR_FIELD = "pk"
VEGA_ACTION_LINK_SEPARATOR = " | "
VEGA_CHANGE_PASSWORD_LABEL = "change password"

# exceptions
VEGA_INVALID_ACTION = "Invalid Action"

# widgets
VEGA_DATE_WIDGET = "vega_admin.widgets.VegaDateWidget"
VEGA_DATETIME_WIDGET = "vega_admin.widgets.VegaDateTimeWidget"
VEGA_TIME_WIDGET = "vega_admin.widgets.VegaTimeWidget"

# contrib
# users
VEGA_USERNAME_HELP_TEXT = (
    "Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
)
VEGA_OPTIONAL_TXT = "Optional."
VEGA_EMAIL_OR_USERNAME_REQUIRED_TXT = "You must provide one of email or username"
