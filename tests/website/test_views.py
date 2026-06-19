from django.test import TestCase, Client
from website.models import Machine, Testimonial, ContactInquiry, Category


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
        response = self.client.get("/solutions/GP-TEST-10/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "website/solution_detail.html")
        self.assertContains(response, "GP-TEST-10")
        
        # Test 404 for non-existing model
        response_404 = self.client.get("/solutions/GP-UNKNOWN/")
        self.assertEqual(response_404.status_code, 404)

