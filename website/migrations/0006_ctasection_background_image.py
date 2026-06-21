# Generated manually to add CTA background images.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_ctasection"),
    ]

    operations = [
        migrations.AddField(
            model_name="ctasection",
            name="background_image",
            field=models.ImageField(blank=True, null=True, upload_to="cta_sections/"),
        ),
    ]
