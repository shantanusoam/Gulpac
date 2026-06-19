from django.test import TestCase, Client


class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_returns_200(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_uses_template(self):
        response = self.client.get("/")
        self.assertTemplateUsed(response, "website/home.html")
