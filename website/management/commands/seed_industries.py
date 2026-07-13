from pathlib import Path

from django.core.files import File
from django.core.management.base import BaseCommand

from website.models import Industry

STATIC_INDUSTRIES_DIR = (
    Path(__file__).resolve().parents[2] / "static" / "images" / "industries"
)

INDUSTRIES_DATA = [
    {
        "title": "Food Industry",
        "image": "food.jpg",
        "detail_image": "food-detail.jpg",
        "bullet_points": [
            "Ready to Eat Boxes",
            "Spice Boxes",
            "Sweet Boxes",
            "Dry Fruits",
        ],
        "order": 1,
    },
    {
        "title": "Pharma Industry",
        "image": "pharma.jpg",
        "detail_image": None,
        "bullet_points": [
            "Soap Boxes",
            "Toothpaste",
            "Vials",
            "Ointments",
        ],
        "order": 2,
    },
    {
        "title": "Cosmetics Industry",
        "image": "cosmetics.jpg",
        "detail_image": None,
        "bullet_points": [
            "Beauty Products",
            "Bonding of Foam",
            "Plastic Components",
        ],
        "order": 3,
    },
    {
        "title": "Paper Industry",
        "image": "paper.jpg",
        "detail_image": None,
        "bullet_points": [
            "Tissue Paper Boxes",
            "Paper Bags",
            "Corrugated Boxes",
            "A4 Paper Reams",
        ],
        "order": 4,
    },
    {
        "title": "Textile Industry",
        "image": "textile.jpg",
        "detail_image": None,
        "bullet_points": [
            "Pasting of Velcro on Fabric",
            "Textile Packaging",
        ],
        "order": 5,
    },
    {
        "title": "Mattress Industry",
        "image": "mattress.jpg",
        "detail_image": None,
        "bullet_points": [
            "Bonding of multiple layers of foam in a mattress",
            "Foam Assembly",
        ],
        "order": 6,
    },
    {
        "title": "Wire Industry",
        "image": "wire.jpg",
        "detail_image": None,
        "bullet_points": [
            "Wire Coil Boxes",
            "Cable Packaging",
        ],
        "order": 7,
    },
    {
        "title": "Automobile Industry",
        "image": "automobile.jpg",
        "detail_image": None,
        "bullet_points": [
            "Air Filters",
            "Head Lights",
            "Automotive Parts Packaging",
        ],
        "order": 8,
    },
]


class Command(BaseCommand):
    help = "Seed industries from bundled static images and default copy"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing industries before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            for industry in Industry.objects.all():
                if industry.image:
                    industry.image.delete(save=False)
                if industry.detail_image:
                    industry.detail_image.delete(save=False)
            Industry.objects.all().delete()

        created = 0
        for data in INDUSTRIES_DATA:
            industry, was_created = Industry.objects.get_or_create(
                title=data["title"],
                defaults={
                    "bullet_points": data["bullet_points"],
                    "order": data["order"],
                    "is_active": True,
                    "show_on_home": True,
                },
            )
            if not was_created:
                industry.bullet_points = data["bullet_points"]
                industry.order = data["order"]
                industry.is_active = True
                industry.show_on_home = True

            image_path = STATIC_INDUSTRIES_DIR / data["image"]
            if image_path.exists():
                with image_path.open("rb") as image_file:
                    industry.image.save(data["image"], File(image_file), save=False)

            detail_name = data.get("detail_image")
            if detail_name:
                detail_path = STATIC_INDUSTRIES_DIR / detail_name
                if detail_path.exists():
                    with detail_path.open("rb") as detail_file:
                        industry.detail_image.save(detail_name, File(detail_file), save=False)

            industry.save()
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} industries."))
