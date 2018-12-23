"""
Views module
"""
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.urls import path, reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from braces.views import (FormMessagesMixin, LoginRequiredMixin,
                          PermissionRequiredMixin)
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin

from vega_admin.forms import ListViewSearchForm
from vega_admin.mixins import (CRUDURLsMixin, DeleteViewMixin,
                               ListViewSearchMixin, ObjectURLPatternMixin,
                               PageTitleMixin, SimpleURLPatternMixin,
                               VegaFormMixin, VerboseNameMixin)
from vega_admin.utils import get_modelform, get_table


# pylint: disable=too-many-ancestors
class VegaListView(
        VerboseNameMixin,
        ListViewSearchMixin,
        PageTitleMixin,
        CRUDURLsMixin,
        ExportMixin,
        SingleTableView,
        SimpleURLPatternMixin,
        ListView,):
    """
    vega-admin Generic List View
    """

    template_name = "vega_admin/basic/list.html"


class VegaCreateView(
        FormMessagesMixin,
        PageTitleMixin,
        VerboseNameMixin,
        VegaFormMixin,
        CRUDURLsMixin,
        SimpleURLPatternMixin,
        CreateView,):
    """
    vega-admin Generic Create View
    """

    template_name = "vega_admin/basic/create.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_CREATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaUpdateView(
        FormMessagesMixin,
        PageTitleMixin,
        VerboseNameMixin,
        VegaFormMixin,
        CRUDURLsMixin,
        ObjectURLPatternMixin,
        UpdateView,):
    """
    vega-admin Generic Update View
    """

    template_name = "vega_admin/basic/update.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_UPDATE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaDeleteView(
        FormMessagesMixin,
        PageTitleMixin,
        VerboseNameMixin,
        DeleteViewMixin,
        CRUDURLsMixin,
        ObjectURLPatternMixin,
        DeleteView,):
    """
    vega-admin Generic Delete View
    """

    template_name = "vega_admin/basic/delete.html"
    form_valid_message = _(settings.VEGA_FORM_VALID_DELETE_TXT)
    form_invalid_message = _(settings.VEGA_FORM_INVALID_TXT)


class VegaCRUDView:  # pylint: disable=too-many-public-methods
    """
    Creates generic CRUD views for a model automagically

    The intention is for you to give it at least a model and get back an entire
    set of CRUD views, with everyhting you need to start doing CRUD actions
    straight away.
    """

    actions = settings.VEGA_DEFAULT_ACTIONS
    protected_actions = actions  # actions that require login
    permissions_actions = actions
    view_classes = {}
    list_fields = None
    search_fields = None
    search_form_class = ListViewSearchForm
    form_fields = None
    create_fields = None
    update_fields = None
    table_attrs = None
    table_actions = None
    form_class = None
    create_form_class = None
    update_form_class = None
    table_class = None
    paginate_by = 25
    crud_path = None

    def __init__(self, model=None):
        """
        Initialize!
        """
        if model is not None:
            self.model = model
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label

        if self.crud_path is None:
            self.crud_path = self.model._meta.label_lower

    def get_actions(self):
        """Get actions"""
        custom_actions = self.get_view_classes().keys()
        custom_actions = [_ for _ in custom_actions if _ not in self.actions]
        return self.actions + custom_actions

    def get_view_classes(self):  # pylint: disable=no-self-use
        """
        Returns the available views
        """
        return self.view_classes

    def get_protected_actions(self):
        """Get list of actions that have login protection"""
        if isinstance(self.protected_actions, list):
            return self.protected_actions
        return []

    def get_permissions_actions(self):
        """Get list of actions that have permissions protection"""
        if isinstance(self.permissions_actions, list):
            return self.permissions_actions
        return []

    def get_search_fields(self):
        """Get search fields for list view"""
        return self.search_fields

    def get_search_form_class(self):
        """Get search form for list view"""
        return self.search_form_class

    def get_createform_fields(self):
        """
        Get fields for create form
        """
        if self.create_fields:
            return self.create_fields
        if self.form_fields:
            return self.form_fields

        return None

    def get_createform_class(self):
        """
        Get form class for create view
        """
        if self.create_form_class:
            return self.create_form_class
        if self.form_class:
            return self.form_class

        return get_modelform(
            model=self.model, fields=self.get_createform_fields())

    def get_updateform_fields(self):
        """
        Get fields for update form
        """
        if self.update_fields:
            return self.update_fields
        if self.form_fields:
            return self.form_fields

        return None

    def get_updateform_class(self):
        """
        Get form class for create view
        """
        if self.update_form_class:
            return self.update_form_class
        if self.form_class:
            return self.form_class

        return get_modelform(
            model=self.model, fields=self.get_updateform_fields())

    def get_table_actions(self):
        """
        Get the table actions
        """
        return self.table_actions

    def get_table_class(self):
        """
        Get the table class
        """
        if self.table_class:
            return self.table_class

        tables_kwargs = {"model": self.model}
        if isinstance(self.list_fields, list):
            tables_kwargs["fields"] = self.list_fields
        if isinstance(self.table_actions, list):
            tables_kwargs["actions"] = self.get_action_urlnames(
                actions=self.table_actions
            )
        if isinstance(self.table_attrs, dict):
            tables_kwargs["attrs"] = self.table_attrs

        return get_table(**tables_kwargs)

    def get_create_view_class(self):  # pylint: disable=no-self-use
        """Get view class for create action"""
        return VegaCreateView

    def get_update_view_class(self):  # pylint: disable=no-self-use
        """Get view class for update action"""
        return VegaUpdateView

    def get_list_view_class(self):  # pylint: disable=no-self-use
        """Get view class for list action"""
        return VegaListView

    def get_delete_view_class(self):  # pylint: disable=no-self-use
        """Get view class for delete action"""
        return VegaDeleteView

    def get_success_url(self):  # pylint: disable=no-self-use
        """Get success_url"""
        return reverse_lazy(
            self.get_url_name_for_action(settings.VEGA_LIST_ACTION))

    def get_cancel_url(self):  # pylint: disable=no-self-use
        """Get cancel_url"""
        return self.get_success_url()

    # pylint: disable=no-self-use
    def enforce_permission_protection(self, view_class: object, action: str):
        """ensures view class has permission protection"""
        has_perms_mixin = issubclass(view_class, PermissionRequiredMixin)
        has_login_mixin = issubclass(view_class, LoginRequiredMixin)

        if not has_login_mixin and not has_perms_mixin:
            # add LoginRequiredMixin and PermissionRequiredMixin
            return type(
                f"{view_class.__name__}{settings.VEGA_PROTECTED_LABEL}",
                (LoginRequiredMixin, PermissionRequiredMixin, view_class,),
                {
                    "permission_required": self.get_permission_for_action(
                        action)
                },
            )

        if not has_login_mixin:
            # add LoginRequiredMixin
            return type(
                f"{view_class.__name__}{settings.VEGA_PROTECTED_LABEL}",
                (LoginRequiredMixin, view_class,),
                {},
            )

        if not has_perms_mixin:
            # in this case the LoginRequiredMixin was set but not
            # PermissionRequiredMixin
            raise ImproperlyConfigured(
                _(f"{settings.VEGA_PERMREQUIRED_NOT_SET_TXT} {view_class.__name__}")  # noqa
            )

        return view_class

    # pylint: disable=no-self-use
    def enforce_login_protection(self, view_class: object):
        """ensures view class has login protection"""
        if issubclass(view_class, LoginRequiredMixin):
            return view_class

        # add LoginRequiredMixin
        return type(
            f"{view_class.__name__}{settings.VEGA_PROTECTED_LABEL}",
            (LoginRequiredMixin, view_class,),
            {},
        )

    def get_permission_for_action(self, action: str):
        """Get permission for action"""
        return f"{self.app_label}.{action}_{self.model_name}"

    def get_default_action_view_classes(self, action: str):
        """Get view class for default actions"""
        if action == settings.VEGA_LIST_ACTION:
            return self.get_list_view_class()
        if action == settings.VEGA_CREATE_ACTION:
            return self.get_create_view_class()
        if action == settings.VEGA_UPDATE_ACTION:
            return self.get_update_view_class()
        if action == settings.VEGA_DELETE_ACTION:
            return self.get_delete_view_class()

        # this action is set as a default action but has no defined view class
        raise Exception(settings.VEGA_INVALID_ACTION)

    def get_view_class_for_action(self, action: str):
        """
        Get the view for an action
        """
        view_classes = self.get_view_classes()
        try:
            # return the view class if found
            view_class = view_classes[action]
        except KeyError:
            if action not in settings.VEGA_DEFAULT_ACTIONS:
                # this action is not supported
                raise Exception(settings.VEGA_INVALID_ACTION)

            # lets get the view class for the default actions
            view_class = self.get_default_action_view_classes(action)
        else:
            if action in self.get_permissions_actions():
                return self.enforce_permission_protection(view_class, action)

            if action in self.get_protected_actions():
                return self.enforce_login_protection(view_class)

            return view_class

        # lets go on and create the view class(es)
        options = {"model": self.model}
        # add some common useful CRUD urls
        options["list_url"] = reverse_lazy(
            self.get_url_name_for_action(settings.VEGA_LIST_ACTION))
        options["create_url"] = reverse_lazy(
            self.get_url_name_for_action(settings.VEGA_CREATE_ACTION))
        options["cancel_url"] = self.get_cancel_url()

        # add the success url
        if action in [
                settings.VEGA_CREATE_ACTION, settings.VEGA_UPDATE_ACTION,
                settings.VEGA_DELETE_ACTION
        ]:
            options["success_url"] = self.get_success_url()

        # add the create form class
        if action == settings.VEGA_CREATE_ACTION:
            options["form_class"] = self.get_createform_class()

        # add the update form class and update url
        if action == settings.VEGA_UPDATE_ACTION:
            options["form_class"] = self.get_updateform_class()
            options["update_url_name"] = self.get_url_name_for_action(
                settings.VEGA_UPDATE_ACTION)

        # add the delete url
        if action == settings.VEGA_DELETE_ACTION:
            options["delete_url_name"] = self.get_url_name_for_action(
                settings.VEGA_DELETE_ACTION)

        # add the table class
        if action == settings.VEGA_LIST_ACTION:
            options["table_class"] = self.get_table_class()
            options["search_fields"] = self.get_search_fields()
            options["form_class"] = self.get_search_form_class()
            options["paginate_by"] = self.paginate_by

        inherited_classes = (view_class,)

        # permissions and login protection
        if action in self.get_permissions_actions():
            inherited_classes = (
                LoginRequiredMixin,
                PermissionRequiredMixin,
                view_class,
            )
            options["permission_required"] = self.get_permission_for_action(
                action)
        elif action in self.get_protected_actions():
            inherited_classes = (LoginRequiredMixin, view_class,)

        # create and return the View class
        view_label = settings.VEGA_VIEW_LABEL
        return type(
            f"{self.model_name.title()}{action.title()}{view_label}",
            inherited_classes,  # the classes that we should inherit
            options,
        )

    # pylint: disable=no-self-use
    def get_url_name_for_action(self, action: str):
        """
        Returns the url name for the action
        """
        return f"{self.crud_path}-{action}"

    def get_action_urlname(self, action: str):
        """
        Get tuple of action and url name
        """
        return (action, self.get_url_name_for_action(action))

    def get_action_urlnames(self, actions: list = None):
        """
        Get list of tuples of (action, url_name)
        """
        if actions is None:
            actions = self.get_actions()
        return [self.get_action_urlname(_) for _ in actions]

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

    def url_patterns(self, actions: list = None):
        """
        Returns the URL patters for the selected actions in this CRUD view
        """
        if actions is None:
            actions = self.get_actions()
        urls = []
        for action in actions:
            view_class = self.get_view_class_for_action(action=action)
            pattern = self.get_url_pattern_for_action(view_class, action)
            url_name = self.get_url_name_for_action(action=action)
            urls.append(path(pattern, view_class.as_view(), name=url_name))

        return urls
