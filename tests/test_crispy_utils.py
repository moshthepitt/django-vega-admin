"""module for crispy_utils tests."""
from django.conf import settings
from django.template import Context, Template
from django.test import TestCase, override_settings

from vega_admin.crispy_utils import get_form_actions, get_form_helper_class, get_layout

from tests.artist_app.forms import PlainArtistForm


@override_settings(
    ROOT_URLCONF="tests.artist_app.urls", VEGA_ACTION_COLUMN_NAME="Actions"
)
class TestCrispyUtils(TestCase):
    """Test class for crispy utils."""

    def test_get_form_actions_no_cancel(self):
        """Test get_form_actions with no cancel."""
        form_helper = get_form_helper_class()
        layout = get_layout(["name"])
        form_actions = get_form_actions(cancel_url=None, button_div_css_class="xxx")
        layout.append(form_actions)
        form_helper.layout = layout
        template = Template(
            """
            {% load crispy_forms_tags %}
            {% crispy form form_helper %}
        """
        )
        context = Context({"form": PlainArtistForm(), "form_helper": form_helper})
        html = template.render(context)

        expected_html = """
        <div class="col-md-12">
            <div class="xxx">
                <input
                    type="submit"
                    name="submit"
                    value="Submit"
                    class="btn btn-primary btn-block vega-submit"
                    id="submit-id-submit"
                />
            </div>
        </div>
        """
        assert "vega-cancel" not in html
        assert settings.VEGA_CANCEL_TEXT not in html
        self.assertInHTML(expected_html, html)
