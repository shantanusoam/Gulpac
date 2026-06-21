# Generated manually to add slug-based product detail URLs.

from django.db import migrations, models
from django.utils.text import slugify


def populate_machine_slugs(apps, schema_editor):
    Machine = apps.get_model("website", "Machine")

    for machine in Machine.objects.all():
        if machine.slug:
            continue
        machine.slug = slugify(f"{machine.model_number}-{machine.name}")
        machine.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0007_contactmapsection_contactsection"),
    ]

    operations = [
        migrations.AddField(
            model_name="machine",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.RunPython(populate_machine_slugs, migrations.RunPython.noop),
    ]
