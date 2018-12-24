"""
vega-admin module to test views
"""
from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase, override_settings

from model_mommy import mommy

from vega_admin.views import (VegaCreateView, VegaCRUDView, VegaDeleteView,
                              VegaListView, VegaUpdateView)

from .artist_app.forms import ArtistForm
from .artist_app.models import Artist, Song
from .artist_app.views import (ArtistCreate, ArtistDelete, ArtistListView,
                               ArtistUpdate)


class TestViewsBase(TestCase):
    """
    Base test class for views
    """

    def _song_permissions(self):
        """
        Create permissions
        """
        content_type = ContentType.objects.get_for_model(Song)
        list_permission, _ = Permission.objects.get_or_create(
            codename='list_song',
            content_type=content_type,
            defaults=dict(name='Can List Songs'),
        )
        create_permission, _ = Permission.objects.get_or_create(
            codename='create_song',
            content_type=content_type,
            defaults=dict(name='Can Create Songs'),
        )
        update_permission, _ = Permission.objects.get_or_create(
            codename='update_song',
            content_type=content_type,
            defaults=dict(name='Can Update Songs'),
        )
        delete_permission, _ = Permission.objects.get_or_create(
            codename='delete_song',
            content_type=content_type,
            defaults=dict(name='Can Delete Songs'),
        )
        artists_permission, _ = Permission.objects.get_or_create(
            codename='artists_song',
            content_type=content_type,
            defaults=dict(name='Can List Song Artists'),
        )
        return [list_permission, create_permission, update_permission,
                delete_permission, artists_permission, ]

    def _artist_permissions(self):
        """
        Create permissions
        """
        content_type = ContentType.objects.get_for_model(Artist)
        list_permission, _ = Permission.objects.get_or_create(
            codename='list_artist',
            content_type=content_type,
            defaults=dict(name='Can List Artists'),
        )
        other_permission, _ = Permission.objects.get_or_create(
            codename='other_artist',
            content_type=content_type,
            defaults=dict(name='Can `Other` Artists'),
        )
        return [list_permission, other_permission, ]

    def setUp(self):
        """setUp"""
        super().setUp()
        self.maxDiff = None
        self.user = User.objects.create_user(
            username='mosh',
            email='mosh@example.com',
            password='hunter2',
        )

    def tearDown(self):
        """tearDown"""
        super().setUp()
        Song.objects.all().delete()
        Artist.objects.all().delete()
        Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Song)).delete()
        Permission.objects.filter(
            content_type=ContentType.objects.get_for_model(Artist)).delete()
        User.objects.all().delete()


@override_settings(ROOT_URLCONF="tests.artist_app.urls")
class TestViews(TestViewsBase):
    """
    Test class for views
    """

    def test_vega_crud_view(self):
        """
        Test VegaCRUDView
        """
        default_actions = ["create", "update", "list", "delete"]

        class ArtistCrud(VegaCRUDView):
            model = Artist

        view = ArtistCrud()

        self.assertEqual(Artist, view.model)
        self.assertEqual(
            list(set(default_actions)), list(set(view.get_actions())))
        self.assertEqual("artist_app.artist", view.crud_path)
        self.assertEqual("artist_app", view.app_label)
        self.assertEqual("artist", view.model_name)

        self.assertEqual(
            Artist, view.get_view_class_for_action("create")().model)
        self.assertEqual(
            Artist, view.get_view_class_for_action("update")().model)
        self.assertEqual(
            Artist, view.get_view_class_for_action("delete")().model)
        self.assertEqual(
            Artist, view.get_view_class_for_action("list")().model)

        self.assertIsInstance(
            view.get_view_class_for_action("create")(), VegaCreateView
        )
        self.assertIsInstance(
            view.get_view_class_for_action("update")(), VegaUpdateView
        )
        self.assertIsInstance(
            view.get_view_class_for_action("delete")(), VegaDeleteView
        )
        self.assertIsInstance(
            view.get_view_class_for_action("list")(), VegaListView)

        self.assertEqual(
            f"{view.crud_path}/create/",
            view.get_url_pattern_for_action(
                view.get_view_class_for_action("create"), "create"
            ),
        )
        self.assertEqual(
            f"{view.crud_path}/list/",
            view.get_url_pattern_for_action(
                view.get_view_class_for_action("list"), "list"
            ),
        )
        self.assertEqual(
            f"{view.crud_path}/update/<int:pk>/",
            view.get_url_pattern_for_action(
                view.get_view_class_for_action("update"), "update"
            ),
        )
        self.assertEqual(
            f"{view.crud_path}/delete/<int:pk>/",
            view.get_url_pattern_for_action(
                view.get_view_class_for_action("delete"), "delete"
            ),
        )

        for action in default_actions:
            self.assertEqual(
                f"{view.crud_path}-{action}",
                view.get_url_name_for_action(action)
            )

    def test_vega_list_view(self):
        """
        Test VegaListView
        """
        artist = mommy.make("artist_app.Artist", name="Bob")
        mommy.make("artist_app.Artist", _quantity=7)
        res = self.client.get("/list/artists/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], ArtistListView)
        self.assertIsInstance(res.context["view"], VegaListView)
        self.assertEqual(res.context["object_list"].count(), 8)
        self.assertTemplateUsed(res, "vega_admin/basic/list.html")

        res = self.client.get("/list/artists/?q=Bob")
        self.assertDictEqual({
            "q": "Bob"
        }, res.context["vega_listview_search_form"].initial)
        self.assertEqual(
            list(set(["q", ])),
            list(set(res.context["vega_listview_search_form"].fields.keys()))
        )
        self.assertEqual(res.context["object_list"].count(), 1)
        self.assertEqual(res.context["object_list"].first(), artist)

    def test_vega_create_view(self):
        """
        Test VegaCreateView
        """
        res = self.client.get("/edit/artists/create/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], ArtistForm)
        self.assertIsInstance(res.context["view"], ArtistCreate)
        self.assertIsInstance(res.context["view"], VegaCreateView)
        self.assertTemplateUsed(res, "vega_admin/basic/create.html")
        res = self.client.post("/edit/artists/create/", {"name": "Mosh"})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/edit/artists/create/")
        self.assertQuerysetEqual(Artist.objects.all(), ["<Artist: Mosh>"])
        self.assertTrue(
            settings.VEGA_FORM_VALID_CREATE_TXT in
            res.cookies["messages"].value
        )
        self.assertFalse(
            settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value
        )

        res = self.client.post("/edit/artists/create/", {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value)

    def test_vega_update_view(self):
        """
        Test VegaUpdateView
        """
        artist = mommy.make("artist_app.Artist", name="Bob")
        res = self.client.get(f"/edit/artists/edit/{artist.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], ArtistForm)
        self.assertIsInstance(res.context["view"], ArtistUpdate)
        self.assertIsInstance(res.context["view"], VegaUpdateView)
        self.assertTemplateUsed(res, "vega_admin/basic/update.html")
        res = self.client.post(
            f"/edit/artists/edit/{artist.id}", {"name": "Mosh"})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, f"/edit/artists/edit/{artist.id}")
        artist.refresh_from_db()
        self.assertEqual("Mosh", artist.name)
        self.assertTrue(
            settings.VEGA_FORM_VALID_UPDATE_TXT in
            res.cookies["messages"].value
        )
        self.assertFalse(
            settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value
        )

        res = self.client.post(f"/edit/artists/edit/{artist.id}", {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(
            settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value)

    def test_vega_delete_view(self):
        """
        Test ArtistDelete
        """
        artist = mommy.make("artist_app.Artist", name="Bob")
        res = self.client.get(f"/edit/artists/delete/{artist.id}")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], ArtistDelete)
        self.assertIsInstance(res.context["view"], VegaDeleteView)
        self.assertTemplateUsed(res, "vega_admin/basic/delete.html")
        res = self.client.post(f"/edit/artists/delete/{artist.id}")
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, f"/edit/artists/create/")
        with self.assertRaises(Artist.DoesNotExist):
            artist.refresh_from_db()

        # test what happens when we have a protected related item
        artist2 = mommy.make("artist_app.Artist", name="Coco")
        mommy.make("artist_app.Song", name="Nuts", artist=artist2)
        res = self.client.post(f"/edit/artists/delete/{artist2.id}")
        self.assertTrue(
            settings.VEGA_DELETE_PROTECTED_ERROR_TXT in
            res.cookies["messages"].value
        )
        self.assertTrue(Artist.objects.filter(id=artist2.id).exists())
