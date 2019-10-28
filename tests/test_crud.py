"""
vega-admin module to test views
"""
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings
from django.urls import reverse

from model_mommy import mommy

from .artist_app.forms import ArtistForm, CustomSearchForm
from .artist_app.models import Artist
from .artist_app.tables import ArtistTable
from .artist_app.views import CustomDefaultActions, CustomSongCRUD
from .test_views import TestViewsBase


# pylint: disable=too-many-locals,line-too-long,too-many-statements,too-many-public-methods  # noqa
@override_settings(
    VEGA_ACTION_COLUMN_NAME="Actions",
    ROOT_URLCONF="tests.artist_app.urls",
    VEGA_TEMPLATE="basic",
)
class TestCRUD(TestViewsBase):
    """
    Test class for CRUD views
    """

    def test_url_patterns(self):
        """
        Test that all url patterns work for default actions
        """
        artist = mommy.make("artist_app.Artist", name="Bob")

        self.assertEqual(
            "/artist_app.artist/create/", reverse("artist_app.artist-create")
        )
        self.assertEqual("/artist_app.artist/list/", reverse("artist_app.artist-list"))
        self.assertEqual(
            f"/artist_app.artist/delete/{artist.pk}/",
            reverse("artist_app.artist-delete", kwargs={"pk": artist.pk}),
        )
        self.assertEqual(
            f"/artist_app.artist/view/{artist.pk}/",
            reverse("artist_app.artist-view", kwargs={"pk": artist.pk}),
        )
        self.assertEqual(
            f"/artist_app.artist/update/{artist.pk}/",
            reverse("artist_app.artist-update", kwargs={"pk": artist.pk}),
        )
        # custom actions
        self.assertEqual("/private-songs/artists/", reverse("private-songs-artists"))
        self.assertEqual("/private-songs/template/", reverse("private-songs-template"))

    def test_create(self):
        """
        Test CRUD create
        """
        url = reverse("artist_app.artist-create")
        res = self.client.post(url, {"name": "Mosh"})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("artist_app.artist-list"))
        self.assertQuerysetEqual(Artist.objects.all(), ["<Artist: Mosh>"])

        # test what happens for a form error
        res = self.client.post(url, {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value)

        # test content
        res = self.client.get(url)
        self.assertEqual("/artist_app.artist/list/", res.context_data["vega_list_url"])
        self.assertEqual(
            "/artist_app.artist/create/", res.context_data["vega_create_url"]
        )
        self.assertEqual(
            "/artist_app.artist/list/", res.context_data["vega_cancel_url"]
        )
        csrf_token = str(res.context["csrf_token"])
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Create professional artist</title></head><body><form id="artist-form" method="post" > <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><div id="div_id_name" class="control-group"> <label for="id_name" class="control-label requiredField"> Name<span class="asteriskField">*</span> </label><div class="controls"> <input type="text" name="name" maxlength="100" class="textinput textInput" required id="id_name"></div></div><div class="form-actions"><div class="row" ><div class="col-md-12" ><div class="col-md-6" > <a href="/artist_app.artist/list/" class="btn btn-block btn-default vega-cancel"> Cancel </a></div><div class="col-md-6" > <input type="submit" name="submit" value="Submit" class="btn btn-block btn-primary vega-submit" id="submit-id-submit" /></div></div></div></div></form></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_read(self):
        """
        Test CRUD read
        """
        artist = mommy.make("artist_app.Artist", name="tt", id=436)
        url = reverse("artist_app.artist-view", kwargs={"pk": artist.id})

        # test content
        res = self.client.get(url)
        self.assertEqual("/artist_app.artist/list/", res.context_data["vega_list_url"])
        self.assertEqual(
            "/artist_app.artist/create/", res.context_data["vega_create_url"]
        )
        self.assertEqual(artist.name, res.context_data["vega_object_title"])
        self.assertEqual(["id", "name"], res.context_data["vega_read_fields"])
        self.assertDictEqual(
            {"name": artist.name, "ID": artist.id}, res.context_data["vega_object_data"]
        )
        self.assertEqual(
            f"/artist_app.artist/view/{artist.pk}/", res.context_data["vega_read_url"]
        )
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> tt | professional artist</title></head><body><h3>tt</h3> <strong>ID</strong>: 436 <br /> <strong>name</strong>: tt <br /></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_update(self):
        """
        Test CRUD update
        """
        artist = mommy.make("artist_app.Artist")
        url = reverse("artist_app.artist-update", kwargs={"pk": artist.id})
        res = self.client.post(url, {"id": artist.id, "name": "Pitt"})
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("artist_app.artist-list"))
        artist.refresh_from_db()
        self.assertEqual("Pitt", artist.name)

        # test what happens for a form error
        res = self.client.post(url, {})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(settings.VEGA_FORM_INVALID_TXT in res.cookies["messages"].value)

        # test content
        res = self.client.get(url)
        self.assertEqual("/artist_app.artist/list/", res.context_data["vega_list_url"])
        self.assertEqual(
            "/artist_app.artist/create/", res.context_data["vega_create_url"]
        )
        self.assertEqual(
            "/artist_app.artist/list/", res.context_data["vega_cancel_url"]
        )
        self.assertEqual(artist.name, res.context_data["vega_object_title"])
        self.assertEqual(
            f"/artist_app.artist/update/{artist.pk}/",
            res.context_data["vega_update_url"],
        )
        csrf_token = str(res.context["csrf_token"])
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Update professional artist</title></head><body><form id="artist-form" method="post" > <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><div id="div_id_name" class="control-group"> <label for="id_name" class="control-label requiredField"> Name<span class="asteriskField">*</span> </label><div class="controls"> <input type="text" name="name" value="Pitt" maxlength="100" class="textinput textInput" required id="id_name"></div></div><div class="form-actions"><div class="row" ><div class="col-md-12" ><div class="col-md-6" > <a href="/artist_app.artist/list/" class="btn btn-block btn-default vega-cancel"> Cancel </a></div><div class="col-md-6" > <input type="submit" name="submit" value="Submit" class="btn btn-block btn-primary vega-submit" id="submit-id-submit" /></div></div></div></div></form></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_delete(self):
        """
        Test CRUD delete
        """
        artist = mommy.make("artist_app.Artist")
        url = reverse("artist_app.artist-delete", kwargs={"pk": artist.id})
        res = self.client.post(url)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse("artist_app.artist-list"))
        with self.assertRaises(Artist.DoesNotExist):
            artist.refresh_from_db()

        # test what happens when we have a protected related item
        artist2 = mommy.make("artist_app.Artist", name="Coco")
        mommy.make("artist_app.Song", name="Nuts", artist=artist2)
        url2 = reverse("artist_app.artist-delete", kwargs={"pk": artist2.id})
        res = self.client.post(url2)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(
            res, reverse("artist_app.artist-delete", kwargs={"pk": artist2.id})
        )
        self.assertTrue(
            settings.VEGA_DELETE_PROTECTED_ERROR_TXT in res.cookies["messages"].value
        )
        self.assertTrue(Artist.objects.filter(id=artist2.id).exists())

        # test content
        res = self.client.get(url2)
        self.assertEqual("/artist_app.artist/list/", res.context_data["vega_list_url"])
        self.assertEqual(
            "/artist_app.artist/create/", res.context_data["vega_create_url"]
        )
        self.assertEqual(
            "/artist_app.artist/list/", res.context_data["vega_cancel_url"]
        )
        self.assertEqual(str(artist2), res.context_data["vega_object_title"])
        self.assertEqual(
            f"/artist_app.artist/delete/{artist2.pk}/",
            res.context_data["vega_delete_url"],
        )
        csrf_token = str(res.context["csrf_token"])
        html = f"""<!doctype html> <html lang="en"> <head> <meta charset="utf-8"> <title> Delete professional artist </title> </head> <body> <form action="" method="post"> <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"> <p>Are you sure you want to delete "Coco"?</p> <input type="submit" value="Confirm" /> </form> </body> </html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_list(self):
        """
        Test CRUD list
        """
        # make 3 objects
        mommy.make("artist_app.Artist", name="Mosh", id="60")
        mommy.make("artist_app.Artist", name="Tranx", id="70")
        mommy.make("artist_app.Artist", name="Eddie", id="80")

        url = reverse("artist_app.artist-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertEqual("/artist_app.artist/list/", res.context_data["vega_list_url"])
        self.assertEqual(
            "/artist_app.artist/create/", res.context_data["vega_create_url"]
        )

        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> professional artists</title></head><body><div class="table-container"><table class="table"><thead ><tr><th class="orderable"> <a href="?sort=id">ID</a></th><th class="orderable"> <a href="?sort=name">Name</a></th><th > Actions</th></tr></thead><tbody ><tr class="even"><td >80</td><td >Eddie</td><td ><a href='/artist_app.artist/view/80/' class='vega-action'>view</a> | <a href='/artist_app.artist/update/80/' class='vega-action'>update</a> | <a href='/artist_app.artist/delete/80/' class='vega-action'>delete</a></td></tr><tr class="odd"><td >60</td><td >Mosh</td><td ><a href='/artist_app.artist/view/60/' class='vega-action'>view</a> | <a href='/artist_app.artist/update/60/' class='vega-action'>update</a> | <a href='/artist_app.artist/delete/60/' class='vega-action'>delete</a></td></tr><tr class="even"><td >70</td><td >Tranx</td><td ><a href='/artist_app.artist/view/70/' class='vega-action'>view</a> | <a href='/artist_app.artist/update/70/' class='vega-action'>update</a> | <a href='/artist_app.artist/delete/70/' class='vega-action'>delete</a></td></tr></tbody></table></div></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_custom_views(self):
        """Test custom views"""
        self.client.force_login(self.user)

        artists_view_url = reverse("private-songs-artists")
        res = self.client.get(artists_view_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], CustomSongCRUD.CustomListView)

        template_view_url = reverse("private-songs-template")
        res = self.client.get(template_view_url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], CustomSongCRUD.FooView)

    def test_custom_default_views(self):
        """Test custom default views"""

        artist = mommy.make("artist_app.Artist")
        url = reverse("custom-default-actions-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], CustomDefaultActions.CustomListView)

        url = reverse("custom-default-actions-create")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(
            res.context["view"], CustomDefaultActions.CustomCreateView
        )

        url = reverse("custom-default-actions-update", kwargs={"pk": artist.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(
            res.context["view"], CustomDefaultActions.CustomUpdateView
        )

        url = reverse("custom-default-actions-view", kwargs={"pk": artist.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["view"], CustomDefaultActions.CustomReadView)

        url = reverse("custom-default-actions-delete", kwargs={"pk": artist.pk})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(
            res.context["view"], CustomDefaultActions.CustomDeleteView
        )

    def test_list_options(self):
        """
        Test CRUD list with configuration options
        """
        # make 3 objects
        artist = mommy.make("artist_app.Artist", name="Mosh", id="60")
        mommy.make("artist_app.Song", name="Song 1", artist=artist, id="31")
        mommy.make("artist_app.Song", name="Song 2", artist=artist, id="32")
        mommy.make("artist_app.Song", name="Song 3", artist=artist, id="33")

        url = reverse("artist_app.song-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Songs</title></head><body><div class="table-container"><table class="song-table"><thead ><tr><th class="orderable"> <a href="?sort=name">Name</a></th><th class="orderable"> <a href="?sort=artist">Artist</a></th><th > Actions</th></tr></thead><tbody ><tr class="even"><td >Song 1</td><td >Mosh</td><td ><a href='/artist_app.song/create/' class='vega-action'>create</a> | <a href='/artist_app.song/update/31/' class='vega-action'>update</a> | <a href='/artist_app.song/delete/31/' class='vega-action'>delete</a></td></tr><tr class="odd"><td >Song 2</td><td >Mosh</td><td ><a href='/artist_app.song/create/' class='vega-action'>create</a> | <a href='/artist_app.song/update/32/' class='vega-action'>update</a> | <a href='/artist_app.song/delete/32/' class='vega-action'>delete</a></td></tr><tr class="even"><td >Song 3</td><td >Mosh</td><td ><a href='/artist_app.song/create/' class='vega-action'>create</a> | <a href='/artist_app.song/update/33/' class='vega-action'>update</a> | <a href='/artist_app.song/delete/33/' class='vega-action'>delete</a></td></tr></tbody></table></div></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_create_options(self):
        """
        Test CRUD create with options
        """
        url = reverse("artist_app.song-create")
        # test content
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        csrf_token = str(res.context["csrf_token"])
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Create Song</title></head><body><form id="song-form" method="post" > <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><div id="div_id_name" class="control-group"> <label for="id_name" class="control-label requiredField"> Name<span class="asteriskField">*</span> </label><div class="controls"> <input type="text" name="name" maxlength="100" class="textinput textInput" required id="id_name"></div></div><div id="div_id_artist" class="control-group"> <label for="id_artist" class="control-label requiredField"> Artist<span class="asteriskField">*</span> </label><div class="controls"> <select name="artist" class="select" required id="id_artist"><option value="" selected>---------</option></select></div></div><div class="form-actions"><div class="row" ><div class="col-md-12" ><div class="col-md-6" > <a href="/artist_app.song/list/" class="btn btn-block btn-default vega-cancel"> Cancel </a></div><div class="col-md-6" > <input type="submit" name="submit" value="Submit" class="btn btn-block btn-primary vega-submit" id="submit-id-submit" /></div></div></div></div></form></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_read_options(self):
        """
        Test CRUD update with options
        """
        artist = mommy.make("artist_app.Artist", name="Mosh")
        song = mommy.make("artist_app.Song", name="Song 1", artist=artist)
        url = reverse("artist_app.song-view", kwargs={"pk": song.id})
        # test content
        res = self.client.get(url)
        self.assertEqual(["name", "artist"], res.context_data["vega_read_fields"])
        self.assertDictEqual(
            {"name": song.name, "artist": str(artist)},
            res.context_data["vega_object_data"],
        )
        self.assertEqual(res.status_code, 200)
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Song 1 | Song</title></head><body><h3>Song 1</h3> <strong>name</strong>: Song 1 <br /> <strong>artist</strong>: Mosh <br /></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_update_options(self):
        """
        Test CRUD update with options
        """
        artist = mommy.make("artist_app.Artist", name="Mosh")
        song = mommy.make("artist_app.Song", name="Song 1", artist=artist)
        url = reverse("artist_app.song-update", kwargs={"pk": song.id})
        # test content
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        csrf_token = str(res.context["csrf_token"])
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title> Update Song</title></head><body><form id="song-form" method="post" > <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}"><div id="div_id_name" class="control-group"> <label for="id_name" class="control-label requiredField"> Name<span class="asteriskField">*</span> </label><div class="controls"> <input type="text" name="name" value="Song 1" maxlength="100" class="textinput textInput" required id="id_name"></div></div><div class="form-actions"><div class="row" ><div class="col-md-12" ><div class="col-md-6" > <a href="/artist_app.song/list/" class="btn btn-block btn-default vega-cancel"> Cancel </a></div><div class="col-md-6" > <input type="submit" name="submit" value="Submit" class="btn btn-block btn-primary vega-submit" id="submit-id-submit" /></div></div></div></div></form></body></html>"""  # noqa
        self.assertHTMLEqual(html, res.content.decode("utf-8"))

    def test_custom_form_and_table_class(self):
        """
        Test custom form and table class
        """
        artist = mommy.make("artist_app.Artist", name="Mosh")
        create_url = reverse("custom-artist-create")
        update_url = reverse("custom-artist-update", kwargs={"pk": artist.id})
        list_url = reverse("custom-artist-list")

        create_res = self.client.get(create_url)
        self.assertEqual(ArtistForm, create_res.context["view"].form_class)

        update_res = self.client.get(update_url)
        self.assertEqual(ArtistForm, update_res.context["view"].form_class)

        list_res = self.client.get(list_url)
        self.assertEqual(ArtistTable, list_res.context["view"].table_class)
        self.assertEqual(["name"], list_res.context["view"].search_fields)
        self.assertEqual(CustomSearchForm, list_res.context["view"].form_class)

    def test_paginate_by(self):
        """
        Test paginate_by
        """
        mommy.make("artist_app.Artist", _quantity=20)
        list_url = reverse("custom-artist-list")
        list_res = self.client.get(list_url)
        self.assertEqual(list_res.context["object_list"].count(), 10)

    def test_get_permissions(self):
        """Test get_permissions"""
        actions = ["create", "update", "delete", "template", "view", "list", "artists"]
        expected = [f"artist_app.{action}_song" for action in actions]

        self.assertEqual(set(expected), set(CustomSongCRUD().get_permissions()))

    @override_settings(LOGIN_URL="/list/artists/")
    def test_login_protection(self):
        """
        Test login protection
        """
        artist = mommy.make("artist_app.Artist", name="Mosh")
        song = mommy.make("artist_app.Song", name="Song 1", artist=artist)
        create_url = reverse("private-songs-create")
        update_url = reverse("private-songs-update", kwargs={"pk": song.id})
        read_url = reverse("private-songs-view", kwargs={"pk": song.id})
        delete_url = reverse("private-songs-delete", kwargs={"pk": song.id})
        list_url = reverse("private-songs-list")

        # first check that login is required
        create_res = self.client.get(create_url)
        self.assertEqual(302, create_res.status_code)
        self.assertRedirects(create_res, f"/list/artists/?next={create_url}")

        update_res = self.client.get(update_url)
        self.assertEqual(302, update_res.status_code)
        self.assertRedirects(update_res, f"/list/artists/?next={update_url}")

        read_res = self.client.get(read_url)
        self.assertEqual(302, read_res.status_code)
        self.assertRedirects(read_res, f"/list/artists/?next={read_url}")

        delete_res = self.client.get(delete_url)
        self.assertEqual(302, delete_res.status_code)
        self.assertRedirects(delete_res, f"/list/artists/?next={delete_url}")

        list_res = self.client.get(list_url)
        # the list action is not set to be protected
        self.assertEqual(200, list_res.status_code)

        # now login
        self.client.force_login(self.user)

        create_res = self.client.get(create_url)
        self.assertEqual(200, create_res.status_code)
        update_res = self.client.get(update_url)
        self.assertEqual(200, update_res.status_code)
        delete_res = self.client.get(delete_url)
        self.assertEqual(200, delete_res.status_code)
        read_res = self.client.get(read_url)
        self.assertEqual(200, read_res.status_code)
        list_res = self.client.get(list_url)
        self.assertEqual(200, list_res.status_code)

    @override_settings(LOGIN_URL="/list/artists/")
    def test_custom_view_login_protection(self):
        """Test custom views"""
        artists_view_url = reverse("private-songs-artists")
        template_view_url = reverse("private-songs-template")
        res1 = self.client.get(artists_view_url)
        self.assertEqual(res1.status_code, 200)

        res2 = self.client.get(template_view_url)
        self.assertEqual(res2.status_code, 302)
        self.assertRedirects(res2, f"/list/artists/?next={template_view_url}")

        # now login
        self.client.force_login(self.user)
        res1 = self.client.get(artists_view_url)
        self.assertEqual(res1.status_code, 200)

        res2 = self.client.get(template_view_url)
        self.assertEqual(res2.status_code, 200)

    @override_settings(LOGIN_URL="/list/artists/")
    def test_permission_protection(self):
        """
        Test permission protection
        """
        artist = mommy.make("artist_app.Artist", name="Mosh")
        song = mommy.make("artist_app.Song", name="Song 42", artist=artist)
        create_url = reverse("hidden-songs-create")
        update_url = reverse("hidden-songs-update", kwargs={"pk": song.id})
        read_url = reverse("hidden-songs-view", kwargs={"pk": song.id})
        delete_url = reverse("hidden-songs-delete", kwargs={"pk": song.id})
        artists_url = reverse("hidden-songs-artists")
        list_url = reverse("hidden-songs-list")  # not protected
        template_url = reverse("hidden-songs-template")  # not protected

        # first check that login is required
        create_res = self.client.get(create_url)
        self.assertEqual(302, create_res.status_code)
        self.assertRedirects(create_res, f"/list/artists/?next={create_url}")

        update_res = self.client.get(update_url)
        self.assertEqual(302, update_res.status_code)
        self.assertRedirects(update_res, f"/list/artists/?next={update_url}")

        read_res = self.client.get(read_url)
        self.assertEqual(302, read_res.status_code)
        self.assertRedirects(read_res, f"/list/artists/?next={read_url}")

        delete_res = self.client.get(delete_url)
        self.assertEqual(302, delete_res.status_code)
        self.assertRedirects(delete_res, f"/list/artists/?next={delete_url}")

        list_res = self.client.get(list_url)
        self.assertEqual(302, list_res.status_code)
        self.assertRedirects(list_res, f"/list/artists/?next={list_url}")

        artists_res = self.client.get(artists_url)
        self.assertEqual(302, artists_res.status_code)
        self.assertRedirects(artists_res, f"/list/artists/?next={artists_url}")

        # the template action is not set to be protected
        template_res = self.client.get(template_url)
        self.assertEqual(200, template_res.status_code)

        # now login to ensure that even a logged in user needs perms
        alice_user = mommy.make("auth.User", username="alice")
        self.client.force_login(alice_user)

        create_res = self.client.get(create_url)
        self.assertEqual(302, create_res.status_code)
        self.assertRedirects(create_res, f"/list/artists/?next={create_url}")

        update_res = self.client.get(update_url)
        self.assertEqual(302, update_res.status_code)
        self.assertRedirects(update_res, f"/list/artists/?next={update_url}")

        read_res = self.client.get(read_url)
        self.assertEqual(302, read_res.status_code)
        self.assertRedirects(read_res, f"/list/artists/?next={read_url}")

        delete_res = self.client.get(delete_url)
        self.assertEqual(302, delete_res.status_code)
        self.assertRedirects(delete_res, f"/list/artists/?next={delete_url}")

        list_res = self.client.get(list_url)
        self.assertEqual(200, list_res.status_code)

        artists_res = self.client.get(artists_url)
        self.assertEqual(302, artists_res.status_code)
        self.assertRedirects(artists_res, f"/list/artists/?next={artists_url}")

        # the template action is not set to be protected
        template_res = self.client.get(template_url)
        self.assertEqual(200, template_res.status_code)

        # now log in with a user who HAS the permissions
        bob_user = mommy.make("auth.User")
        permissions = self._song_permissions()
        bob_user.user_permissions.add(*permissions)
        bob_user = User.objects.get(pk=bob_user.pk)
        self.client.force_login(bob_user)

        create_res = self.client.get(create_url)
        self.assertEqual(200, create_res.status_code)

        update_res = self.client.get(update_url)
        self.assertEqual(200, update_res.status_code)

        read_res = self.client.get(read_url)
        self.assertEqual(200, read_res.status_code)

        delete_res = self.client.get(delete_url)
        self.assertEqual(200, delete_res.status_code)

        artists_res = self.client.get(artists_url)
        self.assertEqual(200, artists_res.status_code)

        list_res = self.client.get(list_url)
        self.assertEqual(200, list_res.status_code)

        template_res = self.client.get(template_url)
        self.assertEqual(200, template_res.status_code)

    @override_settings(ROOT_URLCONF="tests.artist_app.broken_urls")
    def test_broken_permission_protection(self):
        """Test custom views"""
        bob_user = mommy.make("auth.User")
        permissions = self._song_permissions()
        bob_user.user_permissions.add(*permissions)
        bob_user = User.objects.get(pk=bob_user.pk)
        self.client.force_login(bob_user)

        with self.assertRaises(ImproperlyConfigured):
            reverse("broken-list")

    def test_custom_permission_protection(self):
        """Test custom views"""
        bob_user = mommy.make("auth.User")
        permissions = self._artist_permissions()
        bob_user.user_permissions.add(*permissions)
        bob_user = User.objects.get(pk=bob_user.pk)
        self.client.force_login(bob_user)

        res = self.client.get(reverse("42-list"))
        self.assertEqual(200, res.status_code)

        res = self.client.get(reverse("42-other"))
        self.assertEqual(200, res.status_code)

    def test_external_modelform(self):
        """Test that CRUD views created with external model forms work"""
        artist = mommy.make("artist_app.Artist", name="Plain Jane")

        bob_user = mommy.make("auth.User")
        self.client.force_login(bob_user)

        create_url = reverse("plain-form-create")
        update_url = reverse("plain-form-update", kwargs={"pk": artist.id})

        # create, should not result in exceptions esp. TypeError
        create_res = self.client.get(create_url)
        self.assertEqual(200, create_res.status_code)

        # update, should not result in exceptions esp. TypeError
        update_res = self.client.get(update_url)
        self.assertEqual(200, update_res.status_code)
