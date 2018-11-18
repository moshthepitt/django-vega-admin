"""
vega-admin module to test forms
"""
from django.test import TestCase, override_settings

from vega_admin.forms import ListViewSearchForm


class TestForms(TestCase):
    """
    Test class for forms
    """

    @override_settings(
        VEGA_LISTVIEW_SEARCH_QUERY_TXT="Search now",
        VEGA_LISTVIEW_SEARCH_TXT="Search!",
        VEGA_CRISPY_TEMPLATE_PACK="bootstrap3"
    )
    def test_listview_search_form(self):
        """
        Test ListViewSearchForm
        """
        data = {'q': 'give me peanuts'}
        form = ListViewSearchForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertHTMLEqual(
            """
            <p>
                <label for="id_q">Search Query:</label>
                <input type="text" name="q" value="give me peanuts" id="id_q">
            </p>
            """,
            form.as_p()
        )
