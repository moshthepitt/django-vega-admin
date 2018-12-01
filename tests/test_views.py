"""
vega-admin module to test views
"""
from django.conf import settings
from django.test import TestCase, override_settings
from django.urls import reverse
from model_mommy import mommy

from vega_admin.views import (VegaCreateView, VegaCRUDView, VegaDeleteView,
                              VegaListView, VegaUpdateView)

from .artist_app.forms import ArtistForm
from .artist_app.models import Artist
from .artist_app.views import (ArtistCreate, ArtistDelete, ArtistListView,
                               ArtistUpdate)


@override_settings(
    ROOT_URLCONF='tests.artist_app.urls'
)
class TestViews(TestCase):
    """
    Test class for views
    """

    def test_vega_crud_view(self):
        """
        Test VegaCRUDView
        """
        default_actions = ['create', 'update', 'list', 'delete']

        class ArtistCrud(VegaCRUDView):
            model = Artist

        view = ArtistCrud()

        self.assertEqual(Artist, view.model)
        self.assertEqual(default_actions, view.actions)
        self.assertEqual('artist_app.artist', view.crud_path)
        self.assertEqual('artist_app', view.app_label)
        self.assertEqual('artist', view.model_name)

        self.assertEqual(
            Artist,
            view.get_view_class_for_action('create')().model)
        self.assertEqual(
            Artist,
            view.get_view_class_for_action('update')().model)
        self.assertEqual(
            Artist,
            view.get_view_class_for_action('delete')().model)
        self.assertEqual(
            Artist,
            view.get_view_class_for_action('list')().model)

        self.assertIsInstance(
            view.get_view_class_for_action('create')(), VegaCreateView)
        self.assertIsInstance(
            view.get_view_class_for_action('update')(), VegaUpdateView)
        self.assertIsInstance(
            view.get_view_class_for_action('delete')(), VegaDeleteView)
        self.assertIsInstance(
            view.get_view_class_for_action('list')(), VegaListView)

        self.assertEqual(f"{view.crud_path}/create/",
                         view.get_url_pattern_for_action(
                             view.get_view_class_for_action('create'),
                             'create'))
        self.assertEqual(f"{view.crud_path}/list/",
                         view.get_url_pattern_for_action(
                             view.get_view_class_for_action('list'),
                             'list'))
        self.assertEqual(f"{view.crud_path}/update/<int:pk>/",
                         view.get_url_pattern_for_action(
                             view.get_view_class_for_action('update'),
                             'update'))
        self.assertEqual(f"{view.crud_path}/delete/<int:pk>/",
                         view.get_url_pattern_for_action(
                             view.get_view_class_for_action('delete'),
                             'delete'))

        for action in default_actions:
            self.assertEqual(
                f"{view.crud_path}-{action}",
                view.get_url_name_for_action(action))

    def test_vega_list_view(self):
        """
        Test VegaListView
        """
        artist = mommy.make('artist_app.Artist', name="Bob")
        mommy.make('artist_app.Artist', _quantity=7)
        res = self.client.get('/list/artists/')
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context['view'], ArtistListView)
        self.assertIsInstance(res.context['view'], VegaListView)
        self.assertEqual(res.context['object_list'].count(), 8)
        self.assertTemplateUsed(res, 'vega_admin/basic/list.html')

        res = self.client.get('/list/artists/?q=Bob')
        self.assertEqual(res.context['object_list'].count(), 1)
        self.assertEqual(res.context['object_list'].first(), artist)

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


@override_settings(ROOT_URLCONF='tests.artist_app.urls')
class TestCRUD(TestCase):
    """
    Test class for CRUD views
    """

    def test_url_patterns(self):
        """
        Test that all url patterns work for default actions
        """
        artist = mommy.make('artist_app.Artist', name="Bob")

        self.assertEqual("/artist_app.artist/create/",
                         reverse('artist_app.artist-create'))
        self.assertEqual("/artist_app.artist/list/",
                         reverse('artist_app.artist-list'))
        self.assertEqual(
            f"/artist_app.artist/delete/{artist.pk}/",
            reverse('artist_app.artist-delete', kwargs={'pk': artist.pk}))
        self.assertEqual(
            f"/artist_app.artist/update/{artist.pk}/",
            reverse('artist_app.artist-update', kwargs={'pk': artist.pk}))
