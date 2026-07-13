from django.test import SimpleTestCase, TestCase
from django.contrib.auth import get_user_model

from website.admin import MachineAdminForm
from website.admin_widgets import RichTextEditorWidget
from website.models import Machine, ProductCategory, Category


class TinyMCEWidgetTest(SimpleTestCase):
    def test_rich_text_widget_is_tinymce(self):
        widget = RichTextEditorWidget()
        media_js = str(widget.media)
        self.assertIn("tinymce", media_js.lower())
        self.assertIn("django_tinymce/init_tinymce.js", media_js)

    def test_machine_admin_form_uses_tinymce_for_content_fields(self):
        form = MachineAdminForm()
        for field_name in ("description", "specifications", "features"):
            widget = form.fields[field_name].widget
            self.assertIsInstance(widget, RichTextEditorWidget)
            self.assertIn("tinymce", str(widget.media).lower())


class TinyMCEAdminPageTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@test.com",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.category = ProductCategory.objects.get_or_create(
            code=Category.GLUING,
            defaults={"name": "Gluing Machines", "order": 0},
        )[0]
        self.machine = Machine.objects.create(
            model_number="GP-TINYMCE",
            name="TinyMCE Product",
            category=self.category,
            description="<p>Hello</p>",
            features="<ul><li>One</li></ul>",
            specifications="<ul><li>Speed — 10</li></ul>",
        )

    def test_product_change_page_loads_tinymce(self):
        url = f"/admin/website/machine/{self.machine.pk}/change/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn("tinymce", content.lower())
        self.assertIn("data-mce-conf", content)
        self.assertIn("menubar", content)
