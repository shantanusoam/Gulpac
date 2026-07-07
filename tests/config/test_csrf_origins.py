from django.test import SimpleTestCase

from config.settings import build_csrf_trusted_origins


class BuildCsrfTrustedOriginsTest(SimpleTestCase):
    def test_builds_http_and_https_for_plain_hosts(self):
        origins = build_csrf_trusted_origins(["example.com"])
        self.assertEqual(
            origins,
            ["http://example.com", "https://example.com"],
        )

    def test_includes_non_standard_ports(self):
        origins = build_csrf_trusted_origins(["168.144.92.215"], ports=["8011"])
        self.assertIn("http://168.144.92.215:8011", origins)
        self.assertIn("https://168.144.92.215:8011", origins)
        self.assertIn("http://168.144.92.215", origins)

    def test_skips_standard_ports(self):
        origins = build_csrf_trusted_origins(["example.com"], ports=["80", "443"])
        self.assertEqual(
            origins,
            ["http://example.com", "https://example.com"],
        )

    def test_preserves_explicit_origin_urls(self):
        origins = build_csrf_trusted_origins(
            ["http://168.144.92.215:8011"],
            ports=["8011"],
        )
        self.assertEqual(origins, ["http://168.144.92.215:8011"])
