"""
vega-admin module to test utils
"""
from unittest.mock import patch

from django.conf import settings
from django.forms import CharField, ModelForm
from django.test import TestCase, override_settings

from django_filters import FilterSet
from django_tables2 import Table
from model_mommy import mommy

from vega_admin.utils import (
    customize_modelform,
    get_filterclass,
    get_listview_form,
    get_modelform,
    get_table,
)
from vega_admin.widgets import VegaDateTimeWidget, VegaDateWidget, VegaTimeWidget

from tests.artist_app.forms import ArtistForm, PlainArtistForm, UpdateArtistForm
from tests.artist_app.models import Artist, Song


class TestUtils(TestCase):
    """
    class for testing vega-admin utils
    """

    def test_customize_modelform(self):
        """Test customize_modelform."""
        self.assertEqual(ArtistForm, customize_modelform(ArtistForm))
        self.assertEqual(UpdateArtistForm, customize_modelform(UpdateArtistForm))

        custom_form_class = customize_modelform(PlainArtistForm)
        self.assertTrue(issubclass(custom_form_class, PlainArtistForm))
        self.assertEqual("VegaCustomFormClass", custom_form_class.__name__)

        try:
            custom_form_class(**{settings.VEGA_MODELFORM_KWARG: dict()})
        except TypeError:
            self.fail("Form kwargs have not been set properly")

    def test_get_modelform(self):
        """Test get_modelform"""
        # basic form
        form = get_modelform(model=Artist)
        self.assertTrue(issubclass(form, ModelForm))
        self.assertEqual(Artist, form.model)
        self.assertEqual(["id", "name"], form.Meta.fields)
        # form with all options
        form2 = get_modelform(model=Artist, fields=["name"])
        self.assertEqual(Artist, form2.model)
        self.assertEqual(["name"], form2.Meta.fields)
        self.assertHTMLEqual(
            """<p><label for="id_name">Name:</label> <input type="text" name="name" maxlength="100" required id="id_name"></p>""",  # noqa  pylint: disable=line-too-long
            form().as_p(),
        )

    def test_get_modelform_extra_fields(self):
        """Test get_modelform with extra fields"""
        mommy.make("artist_app.Artist", name="Kylie", id=797)
        form = get_modelform(
            model=Song,
            fields=["artist"],
            extra_fields=[("q", CharField(label="Search Now", required=False))],
        )
        self.assertTrue(issubclass(form, ModelForm))
        self.assertEqual(Song, form.model)
        self.assertEqual(["artist"], form.Meta.fields)
        self.assertHTMLEqual(
            """<p><label for="id_artist">Artist:</label><select name="artist" required id="id_artist"><option value="" selected>---------</option><option value="797">Kylie</option></select></p><p><label for="id_q">Search Now:</label> <input type="text" name="q" id="id_q"></p>""",  # noqa  pylint: disable=line-too-long
            form().as_p(),
        )

    @override_settings(VEGA_DATE_WIDGET="vega_admin.widgets.VegaDateWidget")
    def test_get_modelform_datefield(self):
        """Test DateField output of get_modelform"""
        form = get_modelform(model=Song, fields=["release_date"])
        self.assertIsInstance(form().fields["release_date"].widget, VegaDateWidget)
        self.assertHTMLEqual(
            """<p><label for="id_release_date">Release Date:</label> <input type="date" name="release_date" required id="id_release_date"></p>""",  # noqa  pylint: disable=line-too-long
            form().as_p(),
        )

    @override_settings(VEGA_DATETIME_WIDGET="vega_admin.widgets.VegaDateTimeWidget")
    def test_get_modelform_datetimefield(self):
        """Test DateTimeField output of get_modelform"""
        form = get_modelform(model=Song, fields=["recording_time"])
        self.assertIsInstance(
            form().fields["recording_time"].widget, VegaDateTimeWidget
        )
        self.assertHTMLEqual(
            """<p><label for="id_recording_time">Recording Time:</label> <input type="datetime-local" name="recording_time" required id="id_recording_time"></p>""",  # noqa  pylint: disable=line-too-long
            form().as_p(),
        )

    @override_settings(VEGA_TIME_WIDGET="vega_admin.widgets.VegaTimeWidget")
    def test_get_modelform_timefield(self):
        """Test TimeField output of get_modelform"""
        form = get_modelform(model=Song, fields=["release_time"])
        self.assertIsInstance(form().fields["release_time"].widget, VegaTimeWidget)
        self.assertHTMLEqual(
            """<p><label for="id_release_time">Release Time:</label> <input type="time" name="release_time" required id="id_release_time"></p>""",  # noqa  pylint: disable=line-too-long
            form().as_p(),
        )

    @patch("vega_admin.utils.get_modelform")
    @patch("vega_admin.utils.forms.CharField")
    def test_get_listview_form(  # pylint: disable=no-self-use,bad-continuation
        self, charfield_mock, mock
    ):
        """Test get_listview_form"""
        # we need to mock the return value of CharField so that we can
        # compare the test object with the object produced in get_listview_form
        charfield = CharField(
            label=settings.VEGA_LISTVIEW_SEARCH_QUERY_TXT, required=False
        )
        charfield_mock.return_value = charfield
        search_field = ("q", charfield)

        get_listview_form(model=Song, fields=["artist"])

        # assert that get_modelform is called with the expected params
        mock.assert_called_once_with(
            model=Song, fields=["artist"], extra_fields=[search_field]
        )

    @patch("vega_admin.utils.get_modelform")
    @patch("vega_admin.utils.forms.CharField")
    def test_get_listview_form_include_search(
        self, charfield_mock, mock  # pylint: disable=bad-continuation
    ):  # pylint: disable=no-self-use
        """
        Test get_listview_form with include_search=True
        """
        # we need to mock the return value of CharField so that we can
        # compare the test object with the object produced in get_listview_form
        charfield = CharField(
            label=settings.VEGA_LISTVIEW_SEARCH_QUERY_TXT, required=False
        )
        charfield_mock.return_value = charfield
        search_field = ("q", charfield)

        get_listview_form(model=Song, fields=["artist"], include_search=True)

        # assert that get_modelform is called with the expected params
        mock.assert_called_once_with(
            model=Song, fields=["artist"], extra_fields=[search_field]
        )

    @patch("vega_admin.utils.get_modelform")
    def test_get_listview_form_dont_include_search(
        self, mock  # pylint: disable=bad-continuation
    ):  # pylint: disable=no-self-use
        """
        Test get_listview_form with include_search=False
        """
        get_listview_form(model=Song, fields=["artist"], include_search=False)

        # assert that get_modelform is called with the expected params
        mock.assert_called_once_with(model=Song, fields=["artist"], extra_fields=None)

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
        self.assertEqual(["id", "name"], [_[0] for _ in table.base_columns.items()])

        # table with all options set
        table2 = get_table(model=Artist, fields=["name"], attrs={"class": "mytable"})
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
