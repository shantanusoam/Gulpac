from pathlib import Path

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client

from website.models import (
    HeroSection,
    MissionVisionSection,
    Industry,
    CTASection,
    Machine,
    ProductCategory,
    Testimonial,
    ContactInquiry,
    Category,
)


BASE_DIR = Path(__file__).resolve().parents[2]


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.gluing_category, _ = ProductCategory.objects.get_or_create(
            code=Category.GLUING,
            defaults={"name": "Gluing Machines", "order": 0},
        )
        self.cartonator_category, _ = ProductCategory.objects.get_or_create(
            code=Category.CARTONATOR,
            defaults={"name": "Cartonator Machines", "order": 1},
        )
        self.machine = Machine.objects.create(
            model_number="GP-TEST-10",
            name="Test Gluing Machine",
            category=self.gluing_category,
            image_path="images/machine1.png",
            features="<ul><li>Feature 1</li><li>Feature 2</li></ul>",
            description="<p>Test description</p>",
            specifications="<ul><li><strong>Speed</strong> — 10-20 pcs/min</li></ul>",
            meta_title="Test Gluing Machine SEO",
            meta_description="SEO description for test gluing machine.",
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
        image_bytes = (BASE_DIR / "website" / "static" / "images" / "factory.png").read_bytes()
        self.about_hero = HeroSection.objects.create(
            page_key="about",
            title="About From Admin",
            description="This about page hero is managed from the Django admin.",
            back_link_label="Back to Home",
            back_link_url="/",
            background_image=SimpleUploadedFile("about-hero.png", image_bytes, content_type="image/png"),
        )
        self.mission_vision = MissionVisionSection.objects.create(
            page_key="about",
            mission_title="Mission From Admin",
            mission_description="<p><strong>Mission HTML</strong> from admin.</p>",
            vision_title="Vision From Admin",
            vision_description="<p><em>Vision HTML</em> from admin.</p>",
        )
        self.industry = Industry.objects.create(
            title="Food Industry",
            image=SimpleUploadedFile("factory.png", image_bytes, content_type="image/png"),
            bullet_points=["Ready to Eat Food Boxes", "Spice Boxes"],
            order=1,
            is_active=True,
            show_on_home=True,
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

    def test_home_renders_industries_from_admin(self):
        response = self.client.get("/")
        self.assertContains(response, "Food Industry")
        self.assertContains(response, "Ready to Eat Food Boxes")

    def test_about_returns_200_and_uses_template(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/about.html")
        self.assertContains(response, "About From Admin")
        self.assertContains(response, "Mission From Admin")
        self.assertContains(response, "<strong>Mission HTML</strong> from admin.", html=True)
        self.assertContains(response, "<em>Vision HTML</em> from admin.", html=True)
        self.assertContains(response, "WANT TO SEE OUR")
        self.assertContains(response, "FACTORY SETUP?")
        self.assertContains(response, "Book Demonstration")
        self.assertContains(response, "section-cta-bg.png")

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
        self.assertContains(response, "GET IN")
        self.assertContains(response, "TOUCH")
        self.assertContains(response, "We&#x27;d love to hear from you")
        self.assertContains(response, "Send Message")
        self.assertContains(response, "contact/inqueryherobg.png")
        self.assertContains(response, 'id="contact-form"')

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
        Machine.objects.create(
            model_number="GP-TEST-CB",
            name="Test Cartoner Machine",
            category=self.cartonator_category,
            image_path="images/machine2.png",
            features="<ul><li>Cartoning Feature</li></ul>",
            description="<p>Test description cartoner</p>",
            specifications="<ul><li><strong>Speed</strong> — 50 pcs/min</li></ul>",
        )

        response = self.client.get("/solutions/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Gluing Machine")
        self.assertContains(response, "Test Cartoner Machine")

        response_filtered = self.client.get("/solutions/?category=CARTONATOR")
        self.assertEqual(response_filtered.status_code, 200)
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
        self.assertContains(response, "Feature 1")
        self.assertContains(response, "10-20 pcs/min")
        self.assertContains(response, "Send Enquiry")
        self.assertContains(response, "Test Gluing Machine SEO")

        response_404 = self.client.get("/solutions/gp-unknown/")
        self.assertEqual(response_404.status_code, 404)

    def test_product_feature_list_and_image_url(self):
        self.assertEqual(self.machine.feature_list, ["Feature 1", "Feature 2"])
        self.assertTrue(self.machine.image_url.endswith("images/machine1.png"))
        self.assertEqual(self.machine.description_plain, "Test description")
        self.assertEqual(self.machine.get_absolute_url(), f"/solutions/{self.machine.slug}/")

    def test_product_image_upload_preferred_over_legacy_path(self):
        image_bytes = (BASE_DIR / "website" / "static" / "images" / "factory.png").read_bytes()
        self.machine.product_image = SimpleUploadedFile(
            "product.png",
            image_bytes,
            content_type="image/png",
        )
        self.machine.save()
        self.assertIn("products/", self.machine.image_url)

    def test_product_without_category_still_renders(self):
        orphan = Machine.objects.create(
            model_number="GP-ORPHAN",
            name="Uncategorized Product",
            features="",
            description="",
            specifications="",
        )
        response = self.client.get(f"/solutions/{orphan.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Uncategorized Product")
