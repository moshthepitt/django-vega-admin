"""
vega-admin module to test views
"""
from django.conf import settings
from django.test import TestCase, override_settings

from model_mommy import mommy

from vega_admin.views import VegaCreateView, VegaDeleteView, VegaUpdateView

from .artist_app.forms import ArtistForm
from .artist_app.models import Artist
from .artist_app.views import ArtistCreate, ArtistDelete, ArtistUpdate


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

    def test_vega_update_view(self):
        """
        Test VegaUpdateView
        """
        artist = mommy.make('artist_app.Artist', name="Bob")
        res = self.client.get(f'/edit/artists/edit/{artist.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context['form'], ArtistForm)
        self.assertIsInstance(res.context['view'], ArtistUpdate)
        self.assertIsInstance(res.context['view'], VegaUpdateView)
        self.assertTemplateUsed(res, 'vega_admin/basic/update.html')
        res = self.client.post(
            f'/edit/artists/edit/{artist.id}', {'name': 'Mosh'})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, f'/edit/artists/edit/{artist.id}')
        artist.refresh_from_db()
        self.assertEqual('Mosh', artist.name)
        self.assertTrue(
            settings.VEGA_FORM_VALID_UPDATE_TXT in res.cookies[
                'messages'].value)
        self.assertFalse(
            settings.VEGA_FORM_INVALID_TXT in res.cookies['messages'].value)

        res = self.client.post(f'/edit/artists/edit/{artist.id}', {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            settings.VEGA_FORM_INVALID_TXT in res.cookies['messages'].value)

    def test_vega_delete_view(self):
        """
        Test ArtistDelete
        """
        artist = mommy.make('artist_app.Artist', name="Bob")
        res = self.client.get(f'/edit/artists/delete/{artist.id}')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context['view'], ArtistDelete)
        self.assertIsInstance(res.context['view'], VegaDeleteView)
        self.assertTemplateUsed(res, 'vega_admin/basic/delete.html')
        res = self.client.post(f'/edit/artists/delete/{artist.id}')
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, f'/edit/artists/create/')
        with self.assertRaises(Artist.DoesNotExist):
            artist.refresh_from_db()

        # test what happens when we have a protected related item
        artist2 = mommy.make('artist_app.Artist', name="Coco")
        mommy.make('artist_app.Song', name="Nuts", artist=artist2)
        res = self.client.post(f'/edit/artists/delete/{artist2.id}')
        self.assertTrue(
            settings.VEGA_DELETE_PROTECTED_ERROR_TXT in
            res.cookies['messages'].value)
        self.assertTrue(Artist.objects.filter(id=artist2.id).exists())
