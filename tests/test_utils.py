"""
vega-admin module to test utils
"""
from django.test import TestCase, override_settings

from tests.artist_app.models import Artist

from vega_admin.utils import get_table


class TestUtils(TestCase):
    """
    class for testing vega-admin utils
    """

    @override_settings(VEGA_NOTHING_TO_SHOW="Nothing here")
    def test_get_table(self):
        """
        Test get_table
        """
        # basic table
        table = get_table(model=Artist)
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