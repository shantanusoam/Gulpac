from django.core.management.base import BaseCommand
from website.models import Machine, Testimonial, Category

class Command(BaseCommand):
    help = "Seed the database with demo data"

    def handle(self, *args, **options):
        self.stdout.write("Seeding demo data...")

        # Clear existing data
        Machine.objects.all().delete()
        Testimonial.objects.all().delete()

        # Seed Machines
        machines_data = [
            {
                "model_number": "GP-10",
                "name": "Single Head Gluing Machine",
                "category": Category.GLUING,
                "image_path": "images/machine1.png",
                "features": ["Timer base control", "Auto/Manual system", "Foot paddle operation"],
                "description": "Our entry-level gluing solution, custom-engineered for precision and convenience. Perfect for small to medium batches wishing to minimize glue wastage and ensure zero-leakage sealing.",
                "specifications": {"Speed": "15-20 pcs/min", "Power": "220V, 50Hz", "Weight": "150 kg", "Glue Type": "Hot Melt"},
                "order": 1
            },
            {
                "model_number": "GP-20",
                "name": "Double Head Gluing Machine",
                "category": Category.GLUING,
                "image_path": "images/machine2.png",
                "features": ["Double Nozzle", "Two operators", "Twin foot paddles"],
                "description": "Double high-precision nozzle system that allows two separate operators to work simultaneously. Boosts workshop productivity and optimizes floor space with separate twin controls.",
                "specifications": {"Speed": "30-40 pcs/min", "Power": "220V, 50-60Hz", "Weight": "220 kg", "Glue Type": "Hot Melt / Cold Glue"},
                "order": 2
            },
            {
                "model_number": "GP-1500",
                "name": "Mono Carton Gluing Machine",
                "category": Category.GLUING,
                "image_path": "images/machine1.png",
                "features": ["25-35 boxes/min", "HMI PLC", "Digital temp controller"],
                "description": "Heavy-duty carton gluing solution designed for small to mid-sized box dimensions. Equipped with a digital temperature controller and an intuitive HMI touch interface for speed optimization.",
                "specifications": {"Speed": "25-35 boxes/min", "Power": "415V, 3-Phase", "Control System": "PLC HMI", "Temp Range": "50-250°C"},
                "order": 3
            },
            {
                "model_number": "GP-50",
                "name": "Monocarton Gluing Machine",
                "category": Category.GLUING,
                "image_path": "images/machine2.png",
                "features": ["30-60 pcs/min", "180-200°C temp", "220V power supply"],
                "description": "High-efficiency monocarton gluing unit designed for continuous industrial flows. Achieves clean sealing edges without thermal cracking, maintaining superior aesthetic quality.",
                "specifications": {"Speed": "30-60 pcs/min", "Operating Temp": "180-200°C", "Power": "220V AC", "Weight": "310 kg"},
                "order": 4
            },
            {
                "model_number": "GP-5000",
                "name": "High Speed Mono Carton Gluing Machine",
                "category": Category.GLUING,
                "image_path": "images/machine1.png",
                "features": ["62-85 boxes/min", "Automated production", "High efficiency"],
                "description": "Our state-of-the-art flagship high-speed gluing machine, specialized for massive packaging lines. Minimizes wastage, uses laser scanning checks, and implements fully automated carton folding and sealing.",
                "specifications": {"Speed": "62-85 boxes/min", "Automation": "Fully Automated", "Efficiency": "99.8%", "Rated Power": "4.5 kW"},
                "order": 5
            },
            {
                "model_number": "GP-CB-50",
                "name": "Cartonator Machine for Mono Cartons",
                "category": Category.CARTONATOR,
                "image_path": "images/machine2.png",
                "features": ["30-60 box/min", "Pharma & Food", "Fully automatic"],
                "description": "Specialized cartonator machine designed to support cleanroom demands. Seamlessly combines carton erection, active feeding, high-precision gluing, and output stacking for pharmaceuticals, food, and high-value FMCG.",
                "specifications": {"Speed": "30-60 box/min", "Applications": "Pharmaceuticals & Food", "Operation Mode": "Fully Automatic", "Safety Rating": "Class 100 Compliant"},
                "order": 6
            }
        ]

        for m_data in machines_data:
            Machine.objects.create(**m_data)

        # Seed Testimonials
        testimonials_data = [
            {
                "name": "Rajesh Kumar",
                "company": "India Gate Foods",
                "quote": "Glupac machines have transformed our packaging efficiency. Zero-leakage sealing is a game-changer for our premium products, dramatically reducing product return rates.",
                "rating": 5,
                "order": 1
            },
            {
                "name": "Priya Sharma",
                "company": "Haldirams",
                "quote": "Outstanding customization and support. The machine is custom engineered to fit our exact carton sizes, and the automation speed has boosted our day-to-day packaging throughput.",
                "rating": 5,
                "order": 2
            },
            {
                "name": "Mohammed Ali",
                "company": "Finolex Cables",
                "quote": "Excellent build quality and automation. Our production has increased by 40% with zero downtime. Exceptional customer service and prompt response times.",
                "rating": 5,
                "order": 3
            }
        ]

        for t_data in testimonials_data:
            Testimonial.objects.create(**t_data)

        self.stdout.write(self.style.SUCCESS("Done."))


