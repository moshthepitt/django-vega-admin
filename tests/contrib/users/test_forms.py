"""Test vega_admin.contrib.users.forms module"""

from django.test import TestCase

from vega_admin.contrib.users.forms import AddUserForm


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
            "password": "TestAddUserForm",
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
                username="moshthepitt", password="TestAddUserForm"))

        # weak password
        bad_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "username": "moshthepitt2",
            "email": "mosh@example.com",
            "password": "mosh@example.com",
        }
        form = AddUserForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual('The password is too similar to the email address.',
                         form.errors['password'][0])

        # missing email and username
        bad_data = {
            "first_name": "mosh",
            "last_name": "pitt",
            "password": "TestAddUserForm",
        }
        form = AddUserForm(data=bad_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(1, len(form.errors.keys()))
        self.assertEqual('You must provide one of email or username',
                         form.errors['__all__'][0])

    def test_edituserform(self):
        """
        Test EditUserForm

        """
        self.fail()

    def test_password_change_form(self):
        """
        Test PasswordChangeForm
        """
        self.fail()
