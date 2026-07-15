# Rename Machine.video_iframe_html → video_url without remaking the SQLite table.
#
# Reason: production rows store HTML in features/specifications; remaking the table
# would re-apply the legacy JSON_VALID CHECK from when those columns were JSONFields.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0012_product_backend_fields"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.RenameField(
                    model_name="machine",
                    old_name="video_iframe_html",
                    new_name="video_url",
                ),
                migrations.AlterField(
                    model_name="machine",
                    name="video_url",
                    field=models.TextField(
                        blank=True,
                        default="",
                        help_text=(
                            "YouTube or Vimeo URL for the PDP video section "
                            "(e.g. https://youtu.be/…)."
                        ),
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    sql='ALTER TABLE "website_machine" RENAME COLUMN "video_iframe_html" TO "video_url";',
                    reverse_sql='ALTER TABLE "website_machine" RENAME COLUMN "video_url" TO "video_iframe_html";',
                ),
            ],
        ),
    ]
