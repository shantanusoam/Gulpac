# Generated manually for Machine display & media: image upload + video URL.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0011_industry"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="image",
            field=models.ImageField(
                blank=True,
                help_text="Product image shown on the solutions grid and PDP.",
                null=True,
                upload_to="products/",
            ),
        ),
        migrations.AlterField(
            model_name="machine",
            name="image_path",
            field=models.CharField(
                blank=True,
                default="",
                help_text=(
                    "Legacy static path fallback, e.g., 'images/machine1.png'. "
                    "Prefer Product image upload."
                ),
                max_length=250,
            ),
        ),
        migrations.RenameField(
            model_name="machine",
            old_name="video_iframe_html",
            new_name="video_url",
        ),
        migrations.AlterField(
            model_name="machine",
            name="video_url",
            field=models.CharField(
                blank=True,
                default="",
                help_text=(
                    "YouTube or Vimeo URL for the PDP video section "
                    "(e.g. https://youtu.be/…)."
                ),
                max_length=500,
            ),
        ),
    ]
