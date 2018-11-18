"""
vega-admin module to test mixins
"""
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.views.generic import TemplateView

from vega_admin.mixins import PageTitleMixin, VerboseNameMixin


class TestMixins(TestCase):
    """
    class for testing vega-admin mixins
    """

    def setUp(self):
        self.factory = RequestFactory()

    def get_request(self, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Get a request object
        """
        request = self.factory.get('/')
        request.session = {}
        request.user = AnonymousUser
        return request

    def get_response(self, request, view):
        """
        Get the view's response
        """
        response = view(request)
        return response

    def get_request_response(self, view, *args, **kwargs):
        """
        Returns the request and the response of a view
        """
        request = self.get_request(*args, **kwargs)
        response = self.get_response(request, view)
        return request, response

    def test_page_title_mixin(self):
        """
        Test PageTitleMixin
        """

        class TestView(PageTitleMixin, TemplateView):
            page_title = 'Big bad title'
            template_name = 'example.html'

        _, response = self.get_request_response(TestView.as_view())
        self.assertEqual('Big bad title',
                         response.context_data['vega_page_title'])

    def test_verbose_name_mixin(self):
        """
        Test VerboseNameMixin
        """

        class TestView(VerboseNameMixin, TemplateView):
            model = User
            template_name = 'example.html'

        _, response = self.get_request_response(TestView.as_view())
        self.assertEqual('user', response.context_data['vega_verbose_name'])
        self.assertEqual(
            'users', response.context_data['vega_verbose_name_plural'])
