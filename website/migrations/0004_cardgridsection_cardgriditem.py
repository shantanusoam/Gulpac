# Generated manually for reusable card grid sections.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0003_herosection_page_key"),
    ]

    operations = [
        migrations.CreateModel(
            name="CardGridSection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("page_key", models.CharField(max_length=100)),
                ("section_key", models.CharField(max_length=100)),
                ("title", models.CharField(blank=True, default="", max_length=200)),
                ("description", models.TextField(blank=True, default="")),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Card Grid Section",
                "verbose_name_plural": "Card Grid Sections",
            },
        ),
        migrations.AddConstraint(
            model_name="cardgridsection",
            constraint=models.UniqueConstraint(fields=("page_key", "section_key"), name="unique_card_grid_section"),
        ),
        migrations.CreateModel(
            name="CardGridItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("image", models.ImageField(upload_to="card_grid/")),
                ("bullet_points", models.JSONField(default=list)),
                ("order", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "section",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cards", to="website.cardgridsection"),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
    ]
