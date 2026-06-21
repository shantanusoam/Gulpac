# Generated manually to add admin-managed PDP video embeds.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0008_machine_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="video_iframe_html",
            field=models.TextField(
                blank=True,
                default="",
                help_text="Optional raw iframe HTML for the PDP video section.",
            ),
        ),
    ]
