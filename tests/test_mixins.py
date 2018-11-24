"""
vega-admin module to test mixins
"""
from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from model_mommy import mommy

from vega_admin.mixins import (ListViewSearchMixin, PageTitleMixin,
                               VerboseNameMixin)


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
            """
            Test view
            """
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
            """
            Test view
            """
            model = User
            template_name = 'example.html'

        _, response = self.get_request_response(TestView.as_view())
        self.assertEqual('user', response.context_data['vega_verbose_name'])
        self.assertEqual(
            'users', response.context_data['vega_verbose_name_plural'])

    def test_listview_search_mixin(self):
        """
        Test ListViewSearchMixin
        """
        # make some users
        mommy.make('auth.User', _quantity=2)
        mosh_user = mommy.make('auth.User', first_name='mosh')

        class TestView(ListViewSearchMixin, ListView):
            """
            Test view
            """
            model = User
            search_fields = ['first_name']
            template_name = 'example.html'

        _, response = self.get_request_response(TestView.as_view())

        # the form is in the context data as well as all users
        self.assertTrue('vega_listview_search_form' in response.context_data)
        self.assertEqual(
            list(set([x.id for x in response.context_data['object_list']])),
            list(set([x.id for x in User.objects.all()]))
        )

        # now lets search for mosh
        request = self.factory.get('/?q=mosh')
        request.session = {}
        request.user = AnonymousUser
        response2 = TestView.as_view()(request)
        # we should get back just mosh
        self.assertEqual(1, response2.context_data['object_list'].count())
        self.assertEqual(
            mosh_user, response2.context_data['object_list'].first())
