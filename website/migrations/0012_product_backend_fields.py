import json

from django.db import migrations, models
import django.db.models.deletion


def _features_to_html(value):
    if value is None or value == "" or value == []:
        return ""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    if isinstance(value, list):
        items = "".join(f"<li>{item}</li>" for item in value if str(item).strip())
        return f"<ul>{items}</ul>" if items else ""
    return str(value)


def _specifications_to_html(value):
    if value is None or value == "" or value == {}:
        return ""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    if isinstance(value, dict):
        items = "".join(
            f"<li><strong>{key}</strong> — {val}</li>"
            for key, val in value.items()
            if str(key).strip()
        )
        return f"<ul>{items}</ul>" if items else ""
    return str(value)


def forwards_product_backend(apps, schema_editor):
    ProductCategory = apps.get_model("website", "ProductCategory")
    Machine = apps.get_model("website", "Machine")

    seed_categories = [
        ("GLUING", "Gluing Machines", 0),
        ("CARTONING", "Cartoning Machines", 1),
        ("CARTONATOR", "Cartonator Machines", 2),
        ("SHIPPER", "Shipper Carton Machines", 3),
    ]
    categories_by_code = {}
    for code, name, order in seed_categories:
        category, _ = ProductCategory.objects.get_or_create(
            code=code,
            defaults={"name": name, "order": order, "is_active": True},
        )
        categories_by_code[code] = category

    for machine in Machine.objects.all():
        legacy_code = getattr(machine, "legacy_category", None) or "GLUING"
        machine.category = categories_by_code.get(legacy_code) or categories_by_code["GLUING"]
        machine.features = _features_to_html(machine.features)
        machine.specifications = _specifications_to_html(machine.specifications)
        machine.save(update_fields=["category", "features", "specifications"])


def backwards_product_backend(apps, schema_editor):
    Machine = apps.get_model("website", "Machine")
    for machine in Machine.objects.all():
        machine.legacy_category = machine.category.code if machine.category_id else "GLUING"
        machine.save(update_fields=["legacy_category"])


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0011_industry"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=50, unique=True)),
                ("name", models.CharField(max_length=200)),
                ("order", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Product category",
                "verbose_name_plural": "Product categories",
                "ordering": ["order", "name"],
            },
        ),
        migrations.RenameField(
            model_name="machine",
            old_name="category",
            new_name="legacy_category",
        ),
        migrations.AddField(
            model_name="machine",
            name="brochure",
            field=models.FileField(blank=True, help_text="Optional PDF brochure for this product.", null=True, upload_to="brochure/"),
        ),
        migrations.AddField(
            model_name="machine",
            name="category",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="products",
                to="website.productcategory",
            ),
        ),
        migrations.AddField(
            model_name="machine",
            name="meta_description",
            field=models.TextField(blank=True, default=""),
        ),
        migrations.AddField(
            model_name="machine",
            name="meta_title",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
        migrations.AddField(
            model_name="machine",
            name="product_image",
            field=models.ImageField(
                blank=True,
                help_text="Primary product image shown on listing and detail pages.",
                null=True,
                upload_to="products/",
            ),
        ),
        migrations.AddField(
            model_name="machine",
            name="product_type",
            field=models.CharField(
                choices=[
                    ("not_categorized", "Not Categorized"),
                    ("standard", "Standard"),
                    ("custom", "Custom"),
                ],
                default="not_categorized",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="description",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Supports HTML entered through the admin rich text editor.",
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="features",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Supports HTML entered through the admin rich text editor.",
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="image_path",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Legacy static path fallback, e.g., 'images/machine1.png'. Prefer Product image upload.",
                max_length=250,
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="model_number",
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name="Product SKU ID"),
        ),
        migrations.AlterField(
            model_name="machine",
            name="specifications",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Supports HTML entered through the admin rich text editor.",
            ),
        ),
        migrations.AlterModelOptions(
            name="machine",
            options={"ordering": ["order", "model_number"], "verbose_name": "Product", "verbose_name_plural": "Products"},
        ),
        migrations.RunPython(forwards_product_backend, backwards_product_backend),
        migrations.RemoveField(
            model_name="machine",
            name="legacy_category",
        ),
    ]
