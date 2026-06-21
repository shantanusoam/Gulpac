from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from website.models import HeroSection, CardGridSection, CardGridItem, CTASection, Machine, Testimonial, ContactInquiry, Category


BASE_DIR = Path(__file__).resolve().parents[2]


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some seed data for tests
        self.machine = Machine.objects.create(
            model_number="GP-TEST-10",
            name="Test Gluing Machine",
            category=Category.GLUING,
            image_path="images/machine1.png",
            features=["Feature 1", "Feature 2"],
            description="Test description",
            specifications={"Speed": "10-20 pcs/min"}
        )
        self.testimonial = Testimonial.objects.create(
            name="Test User",
            company="Test Company",
            quote="Great machine!",
            rating=5
        )
        self.hero_section = HeroSection.objects.create(
            page_key="industries",
            title="Industries From Admin",
            description="This content is managed from the Django admin.",
            back_link_label="Back to Home",
            back_link_url="/",
        )
        self.industry_section = CardGridSection.objects.create(
            page_key="industries",
            section_key="industries-grid",
            title="",
            description="",
        )
        image_bytes = (BASE_DIR / "website" / "static" / "images" / "factory.png").read_bytes()
        self.industry_card = CardGridItem.objects.create(
            section=self.industry_section,
            title="Food Industry",
            image=SimpleUploadedFile("factory.png", image_bytes, content_type="image/png"),
            bullet_points=["Ready to Eat Food Boxes", "Spice Boxes"],
        )
        self.cta_section = CTASection.objects.create(
            page_key="industries",
            section_key="industries-cta",
            heading_prefix="DON'T SEE YOUR",
            heading_accent="INDUSTRY LISTED?",
            description="We specialize in custom solutions. Contact us to discuss your specific packaging requirements.",
            background_image=SimpleUploadedFile("component2.png", image_bytes, content_type="image/png"),
            button_label="Contact Us Today",
            button_url="/contact/",
        )

    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_uses_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "website/home.html")
        self.assertContains(response, "Test Gluing Machine")
        self.assertContains(response, "Great machine!")

    def test_about_returns_200_and_uses_template(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/about.html")
        self.assertContains(response, "Pioneering Packaging Excellence")

    def test_industries_returns_200_and_uses_template(self):
        response = self.client.get("/industries/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/industries.html")
        self.assertContains(response, "Industries From Admin")
        self.assertContains(response, "This content is managed from the Django admin.")
        self.assertContains(response, "Food Industry")
        self.assertContains(response, "Ready to Eat Food Boxes")
        self.assertContains(response, "DON&#x27;T SEE YOUR")
        self.assertContains(response, "Contact Us Today")

    def test_contact_get_returns_200(self):
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/contact.html")

    def test_contact_post_creates_inquiry(self):
        self.assertEqual(ContactInquiry.objects.count(), 0)
        
        post_data = {
            "name": "Applicant Name",
            "email": "applicant@test.com",
            "phone": "+919898989898",
            "company": "Applicant Corp",
            "message": "We need customized guidelines and nozzle spacing setup.",
            "machine_interest": "GP-TEST-10"
        }
        response = self.client.post("/contact/", post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactInquiry.objects.count(), 1)
        
        inquiry = ContactInquiry.objects.first()
        self.assertEqual(inquiry.name, "Applicant Name")
        self.assertEqual(inquiry.machine_interest, "GP-TEST-10")

    def test_solutions_list_and_filter(self):
        # Create a cartoner machine
        Machine.objects.create(
            model_number="GP-TEST-CB",
            name="Test Cartoner Machine",
            category=Category.CARTONATOR,
            image_path="images/machine2.png",
            features=["Cartoning Feature"],
            description="Test description cartoner",
            specifications={"Speed": "50 pcs/min"}
        )
        
        # Test full list
        response = self.client.get("/solutions/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Gluing Machine")
        self.assertContains(response, "Test Cartoner Machine")
        
        # Test filtering by Category
        response_filtered = self.client.get("/solutions/?category=CARTONATOR")
        self.assertEqual(response_filtered.status_code, 200)
        # Should contain Cartoner machine but NOT Gluing machine
        self.assertContains(response_filtered, "Test Cartoner Machine")
        self.assertNotContains(response_filtered, "Test Gluing Machine")

    def test_solution_detail_views(self):
        response = self.client.get(f"/solutions/{self.machine.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/solution_detail.html")
        self.assertContains(response, "GP-TEST-10")
        self.assertContains(response, "See It In Action")
        self.assertContains(response, "Main Features")
        self.assertContains(response, "Technical Specifications")
        self.assertContains(response, "Send Enquiry")
        
        # Test 404 for non-existing model
        response_404 = self.client.get("/solutions/gp-unknown/")
        self.assertEqual(response_404.status_code, 404)
