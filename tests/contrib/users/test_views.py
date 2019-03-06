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
