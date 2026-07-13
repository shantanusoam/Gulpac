from django.test import TestCase, Client, override_settings


@override_settings(
    CSRF_TRUSTED_ORIGINS=[
        "http://127.0.0.1:8011",
        "http://localhost:8011",
    ],
    ALLOWED_HOSTS=["127.0.0.1", "localhost"],
)
class ContactCsrfTest(TestCase):
    def setUp(self):
        self.client = Client(HTTP_HOST="127.0.0.1:8011")

    def test_contact_post_succeeds_with_trusted_origin(self):
        response = self.client.post(
            "/contact/",
            {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+919898989898",
                "company": "Test Corp",
                "message": "Need a packaging machine.",
            },
            HTTP_ORIGIN="http://127.0.0.1:8011",
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Thank you! Your inquiry has been submitted.")
