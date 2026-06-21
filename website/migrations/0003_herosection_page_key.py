# Generated manually to replace slug with page_key.

from django.db import migrations, models


def copy_slug_to_page_key(apps, schema_editor):
    HeroSection = apps.get_model("website", "HeroSection")
    for hero in HeroSection.objects.all():
        if not hero.page_key:
            hero.page_key = "industries"
            hero.save(update_fields=["page_key"])


def copy_page_key_to_slug(apps, schema_editor):
    HeroSection = apps.get_model("website", "HeroSection")
    for hero in HeroSection.objects.all():
        hero.slug = hero.page_key
        hero.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0002_herosection"),
    ]

    operations = [
        migrations.AddField(
            model_name="herosection",
            name="page_key",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.RunPython(copy_slug_to_page_key, copy_page_key_to_slug),
        migrations.AlterField(
            model_name="herosection",
            name="page_key",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.RemoveField(
            model_name="herosection",
            name="slug",
        ),
    ]
