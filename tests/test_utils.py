"""
vega-admin module to test utils
"""
from django.forms import ModelForm
from django.test import TestCase, override_settings

from django_filters import FilterSet
from django_tables2 import Table
from tests.artist_app.models import Artist, Song

from vega_admin.utils import get_filterclass, get_modelform, get_table


class TestUtils(TestCase):
    """
    class for testing vega-admin utils
    """

    def test_get_modelform(self):
        """Test get_modelform"""
        # basic form
        form = get_modelform(model=Artist)
        self.assertTrue(issubclass(form, ModelForm))
        self.assertEqual(Artist, form.model)
        self.assertEqual(["id", "name"], form.Meta.fields)
        # form with all options
        form2 = get_modelform(model=Artist, fields=['name'])
        self.assertEqual(Artist, form2.model)
        self.assertEqual(["name"], form2.Meta.fields)

    @override_settings(VEGA_NOTHING_TO_SHOW="Nothing here")
    def test_get_table(self):
        """
        Test get_table
        """
        # basic table
        table = get_table(model=Artist)
        self.assertTrue(issubclass(table, Table))
        self.assertEqual(Artist, table.Meta.model)
        self.assertEqual("Nothing here", table.Meta.empty_text)
        self.assertEqual(
            ["id", "name"], [_[0] for _ in table.base_columns.items()])

        # table with all options set
        table2 = get_table(
            model=Artist, fields=["name"], attrs={"class": "mytable"})
        self.assertEqual(Artist, table2.Meta.model)
        self.assertEqual("Nothing here", table2.Meta.empty_text)
        self.assertEqual(["name"], [_[0] for _ in table2.base_columns.items()])
        self.assertEqual(["id"], table2.Meta.exclude)
        self.assertEqual({"class": "mytable"}, table2.Meta.attrs)
        self.assertEqual(("name", "..."), table2.Meta.sequence)

    def test_get_filterclass(self):
        """Test get_filterclass"""
        filter_class = get_filterclass(model=Song, fields=["artist"])
        self.assertEqual(Song, filter_class.Meta.model)
        self.assertEqual(["artist"], filter_class.Meta.fields)
        self.assertTrue(issubclass(filter_class, FilterSet))
