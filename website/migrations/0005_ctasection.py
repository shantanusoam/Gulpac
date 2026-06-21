# Generated manually for reusable CTA sections.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_cardgridsection_cardgriditem"),
    ]

    operations = [
        migrations.CreateModel(
            name="CTASection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page_key", models.CharField(max_length=100)),
                ("section_key", models.CharField(max_length=100)),
                ("heading_prefix", models.CharField(max_length=200)),
                ("heading_accent", models.CharField(max_length=200)),
                ("description", models.TextField()),
                ("button_label", models.CharField(max_length=100)),
                ("button_url", models.CharField(default="/contact/", max_length=255)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "CTA Section",
                "verbose_name_plural": "CTA Sections",
            },
        ),
        migrations.AddConstraint(
            model_name="ctasection",
            constraint=models.UniqueConstraint(fields=("page_key", "section_key"), name="unique_cta_section"),
        ),
    ]
