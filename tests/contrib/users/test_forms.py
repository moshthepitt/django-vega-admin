"""Test vega_admin.contrib.users.forms module"""

from django.test import TestCase, override_settings
from unittest.mock import patch

from model_mommy import mommy

from vega_admin.contrib.users.forms import (AddUserForm, EditUserForm,
                                            PasswordChangeForm)


@override_settings(
    ROOT_URLCONF="vega_admin.contrib.users.urls", VEGA_TEMPLATE="basic")
class TestForms(TestCase):
    """
    Test class for vega_admin.contrib.users.forms
    """

    def test_adduserform(self):
        """
        Test AddUserForm

        """
        good_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "username": "moshthepitt",
            "email": "mosh@example.com",
            "password": "Miserable-Water-9",
        }

        form = AddUserForm(data=good_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual("mosh", user.first_name)
        self.assertEqual("pitt", user.last_name)
        self.assertEqual("moshthepitt", user.username)
        self.assertEqual("mosh@example.com", user.email)
        self.assertTrue(
            self.client.login(
                username="moshthepitt", password="Miserable-Water-9"))

        # good data no username
        good_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "email": "mosh2@example.com",
            "password": "Bean-Quarrel-0",
        }

        form = AddUserForm(data=good_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual("mosh", user.username)  # was generated

        # weak password
        bad_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "username": "moshthepitt2",
            "email": "mosh3@example.com",
            "password": "mosh@example.com",
        }
        form = AddUserForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual(
            "The password is too similar to the email address.",
            form.errors["password"][0],
        )

        # email not unique
        bad_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "username": "moshthepitt3",
            "email": "mosh@example.com",
            "password": "Every-Actor-1",
        }
        form = AddUserForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual(
            "A user is already registered with this e-mail address.",
            form.errors["email"][0],
        )

        # missing email and username
        bad_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "password": "TestAddUserForm",
        }
        form = AddUserForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual("You must provide one of email or username",
                         form.errors["__all__"][0])

    def test_edituserform(self):
        """
        Test EditUserForm

        """
        user = mommy.make("auth.User")

        good_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "username": "moshthepitt22",
            "email": "mosh22@example.com",
        }
        form = EditUserForm(instance=user, data=good_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual("mosh", user.first_name)
        self.assertEqual("pitt", user.last_name)
        self.assertEqual("moshthepitt22", user.username)
        self.assertEqual("mosh22@example.com", user.email)

    def test_password_change_form(self):
        """
        Test PasswordChangeForm
        """
        user = mommy.make("auth.User", username="softie")

        good_data = {
            "password1": "PasswordChangeForm",
            "password2": "PasswordChangeForm",
        }
        form = PasswordChangeForm(instance=user, data=good_data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertTrue(
            self.client.login(
                username="softie", password="PasswordChangeForm"))

        # weak password
        bad_data = {"password1": "123456789", "password2": "123456789"}
        form = PasswordChangeForm(instance=user, data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual("This password is too common.",
                         form.errors["password2"][0])
        self.assertEqual("This password is entirely numeric.",
                         form.errors["password2"][1])

        # different passwords
        bad_data = {
            "password1": "PasswordChangeForm",
            "password2": "123456789"
        }
        form = PasswordChangeForm(instance=user, data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual("The two password fields didn't match.",
                         form.errors["password2"][0])

    @patch('vega_admin.contrib.users.forms.get_form_actions')
    def test_password_change_form_cancel_url(self, mock):
        """Test cancel url on password change form"""
        user = mommy.make("auth.User")

        good_data = {
            "password1": "PasswordChangeForm",
            "password2": "PasswordChangeForm",
        }
        form = PasswordChangeForm(instance=user, data=good_data)
        self.assertTrue(form.is_valid())
        form.save()

        mock.assert_called_with(cancel_url="/auth.user/list/")
