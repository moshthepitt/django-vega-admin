"""Test filtering"""
from django.contrib.auth.models import User
from django.test import override_settings
from django.urls import reverse

from model_mommy import mommy

from .test_views import TestViewsBase


@override_settings(
    VEGA_ACTION_COLUMN_NAME="Actions",
    ROOT_URLCONF="tests.artist_app.filter_urls",
)
class TestFilters(TestViewsBase):
    """
    Test class for CRUD view filtering
    """

    def test_list_filtering(self):
        """
        Test CRUD list filtering
        """
        # make some sonf objects
        artist1 = mommy.make("artist_app.Artist", name="Mosh")
        artist2 = mommy.make("artist_app.Artist", name="tt")
        mommy.make("artist_app.Song", name="1", artist=artist1)
        mommy.make("artist_app.Song", _quantity=7, artist=artist1)
        mommy.make("artist_app.Song", name="2", artist=artist2)

        bob_user = mommy.make('auth.User')
        permissions = self._song_permissions()
        bob_user.user_permissions.add(*permissions)
        bob_user = User.objects.get(pk=bob_user.pk)
        self.client.force_login(bob_user)

        # using generated filter class
        res = self.client.get(reverse('filters-list'))
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 9)

        res = self.client.get(f"{reverse('filters-list')}?artist={artist1.pk}")
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 8)

        res = self.client.get(f"{reverse('filters-list')}?artist={artist2.pk}")
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 1)

        res = self.client.get(f"{reverse('filters-list')}?name=1")
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 1)

        res = self.client.get(f"{reverse('filters-list')}?name=2")
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 1)

        # using a concrete filter class
        res = self.client.get(
            f"{reverse('filters2-list')}?artist={artist2.pk}")
        self.assertEqual(200, res.status_code)
        self.assertEqual(res.context["object_list"].count(), 1)
