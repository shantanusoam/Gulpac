from django.contrib.auth import get_user_model
from django.test import TestCase

from website.admin import MachineAdminForm
from website.models import Category, Machine, ProductCategory


class ProductAdminEditTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            username="editor",
            email="editor@test.com",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.category = ProductCategory.objects.get_or_create(
            code=Category.GLUING,
            defaults={"name": "Gluing Machines", "order": 0},
        )[0]
        self.machine = Machine.objects.create(
            model_number="GP-20",
            name="Double Head Gluing Machine",
            slug="double-head-gluing-machine",
            category=self.category,
            description="<p>Product</p>",
            features="<ul><li>Feature</li></ul>",
            specifications="<ul><li>Spec</li></ul>",
        )

    def test_edit_form_allows_same_slug_on_existing_product(self):
        form = MachineAdminForm(
            data={
                "model_number": "GP-200",
                "name": self.machine.name,
                "description": self.machine.description,
                "specifications": self.machine.specifications,
                "features": self.machine.features,
                "category": self.category.pk,
                "slug": self.machine.slug,
                "meta_description": "",
                "meta_title": "",
                "product_type": self.machine.product_type,
                "video_url": "",
                "order": self.machine.order,
            },
            instance=self.machine,
        )
        self.assertTrue(form.is_valid(), form.errors)
        product = form.save()
        self.assertEqual(product.pk, self.machine.pk)
        self.assertEqual(product.model_number, "GP-200")
        self.assertEqual(product.slug, "double-head-gluing-machine")
        self.assertEqual(Machine.objects.count(), 1)

    def test_admin_change_view_saves_sku_update_with_existing_slug(self):
        url = f"/admin/website/machine/{self.machine.pk}/change/"
        response = self.client.post(
            url,
            {
                "model_number": "GP-200",
                "name": self.machine.name,
                "description": self.machine.description,
                "specifications": self.machine.specifications,
                "features": self.machine.features,
                "category": self.category.pk,
                "slug": self.machine.slug,
                "meta_description": "",
                "meta_title": "",
                "product_type": self.machine.product_type,
                "video_url": "",
                "order": self.machine.order,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.machine.refresh_from_db()
        self.assertEqual(self.machine.model_number, "GP-200")
        self.assertEqual(self.machine.slug, "double-head-gluing-machine")
        self.assertEqual(Machine.objects.filter(model_number="GP-20").count(), 0)

    def test_duplicate_sku_on_another_product_still_rejected(self):
        Machine.objects.create(
            model_number="GP-200",
            name="Other Product",
            slug="other-product",
            category=self.category,
        )
        form = MachineAdminForm(
            data={
                "model_number": "GP-200",
                "name": self.machine.name,
                "description": self.machine.description,
                "specifications": self.machine.specifications,
                "features": self.machine.features,
                "category": self.category.pk,
                "slug": self.machine.slug,
                "meta_description": "",
                "meta_title": "",
                "product_type": self.machine.product_type,
                "video_url": "",
                "order": self.machine.order,
            },
            instance=self.machine,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("model_number", form.errors)
