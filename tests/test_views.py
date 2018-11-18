"""
vega-admin module to test views
"""
from django.test import TestCase, override_settings
from vega_admin.views import VegaCreateView
from .artist_app.forms import ArtistForm
from .artist_app.views import ArtistCreate
from .artist_app.models import Artist

from django.conf import settings


@override_settings(
    ROOT_URLCONF='tests.artist_app.urls'
)
class TestViews(TestCase):
    """
    Test class for views
    """

    def test_vega_create_view(self):
        """
        Test VegaCreateView
        """
        res = self.client.get('/edit/artists/create/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context['form'], ArtistForm)
        self.assertIsInstance(res.context['view'], ArtistCreate)
        self.assertIsInstance(res.context['view'], VegaCreateView)
        self.assertTemplateUsed(res, 'vega_admin/basic/create.html')
        res = self.client.post('/edit/artists/create/', {'name': 'Mosh'})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, '/edit/artists/create/')
        self.assertQuerysetEqual(Artist.objects.all(), ['<Artist: Mosh>'])
        self.assertTrue(
            settings.VEGA_FORM_VALID_CREATE_TXT in res.cookies[
                'messages'].value)
        self.assertFalse(
            settings.VEGA_FORM_INVALID_TXT in res.cookies['messages'].value)

        res = self.client.post('/edit/artists/create/', {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            settings.VEGA_FORM_INVALID_TXT in res.cookies['messages'].value)
