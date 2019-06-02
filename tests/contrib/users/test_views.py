"""Test vega_admin.contrib.users.forms module"""

from django.test import TestCase, override_settings

from model_mommy import mommy

from vega_admin.contrib.users.forms import PasswordChangeForm
from vega_admin.contrib.users.views import ChangePassword
from vega_admin.views import VegaUpdateView


@override_settings(
    ROOT_URLCONF="vega_admin.contrib.users.urls", VEGA_TEMPLATE="basic")
class TestViews(TestCase):
    """
    Test class for vega_admin.contrib.users.views
    """

    def test_changepassword(self):
        """
        Test ChangePassword

        """
        user = mommy.make("auth.User", username="TestChangePasswordView")
        data = {
            "password1": "Extension-I-School-5",
            "password2": "Extension-I-School-5",
        }

        res = self.client.get(f"/auth.user/change%20password/{user.id}/")
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.context["form"], PasswordChangeForm)
        self.assertIsInstance(res.context["view"], ChangePassword)
        self.assertIsInstance(res.context["view"], VegaUpdateView)
        self.assertTemplateUsed(res, "vega_admin/basic/update.html")
        res = self.client.post(f"/auth.user/change%20password/{user.id}/",
                               data)
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, "/auth.user/list/")
        user.refresh_from_db()
        self.assertTrue(
            self.client.login(
                username="TestChangePasswordView",
                password="Extension-I-School-5"))

    @override_settings(VEGA_FORCE_ORDERING=True)
    def test_list_view_ordering(self):
        """
        Test VEGA_FORCE_ORDERING=True
        """
        mommy.make("auth.User", _quantity=7)
        res = self.client.get("/auth.user/list/")
        self.assertTrue(res.context["object_list"].ordered)
        self.assertEqual("-last_login",
                         res.context["object_list"].query.order_by[0])
        self.assertEqual("first_name",
                         res.context["object_list"].query.order_by[1])

    @override_settings(VEGA_FORCE_ORDERING=False)
    def test_list_view_ordering_off(self):
        """
        Test VEGA_FORCE_ORDERING=False
        """
        mommy.make("auth.User", _quantity=3)
        res = self.client.get("/auth.user/list/")
        self.assertFalse(res.context["object_list"].ordered)
