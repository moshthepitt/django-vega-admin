"""
Module to test that everything is setup okay i.e. no exceptions
"""
from django.test import TestCase


class TestSetup(TestCase):
    """
    Test class for emails
    """

    def test_setup(self):
        """
        Test setup
        """
        self.assertEqual(1, 1)
