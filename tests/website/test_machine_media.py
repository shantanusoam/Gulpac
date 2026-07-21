from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase

from website.models import Machine
from website.video import resolve_video_embed_url


class ResolveVideoEmbedUrlTests(SimpleTestCase):
    def test_youtu_be_short_url(self):
        url = resolve_video_embed_url(
            "https://youtu.be/j5jGpNVVrUI?si=Kzz3-hZWC5NcvXcv"
        )
        self.assertEqual(url, "https://www.youtube.com/embed/j5jGpNVVrUI")

    def test_youtube_watch_url(self):
        url = resolve_video_embed_url(
            "https://www.youtube.com/watch?v=j5jGpNVVrUI&t=12s"
        )
        self.assertEqual(url, "https://www.youtube.com/embed/j5jGpNVVrUI")

    def test_legacy_iframe_html_extracts_src(self):
        html = (
            '<iframe src="https://www.youtube.com/embed/abc123" '
            'title="Demo" allowfullscreen></iframe>'
        )
        self.assertEqual(
            resolve_video_embed_url(html),
            "https://www.youtube.com/embed/abc123",
        )

    def test_empty_and_invalid_return_empty(self):
        self.assertEqual(resolve_video_embed_url(""), "")
        self.assertEqual(resolve_video_embed_url("not-a-url"), "")
        self.assertEqual(resolve_video_embed_url("<iframe></iframe>"), "")


class MachineDisplayMediaTests(TestCase):
    def test_image_url_prefers_product_image_upload(self):
        machine = Machine.objects.create(
            model_number="GP-IMG-1",
            name="Upload Machine",
            image_path="images/machine1.png",
            product_image=SimpleUploadedFile(
                "product.png",
                b"\x89PNG\r\n\x1a\n",
                content_type="image/png",
            ),
        )
        self.assertTrue(machine.image_url.startswith("/media/products/"))

    def test_image_url_falls_back_to_static_path(self):
        machine = Machine.objects.create(
            model_number="GP-IMG-2",
            name="Legacy Path Machine",
            image_path="images/machine2.png",
        )
        self.assertEqual(machine.image_url, "/static/images/machine2.png")

    def test_solution_hero_prefers_dedicated_hero_image(self):
        machine = Machine.objects.create(
            model_number="GP-HERO-1",
            name="Hero Image Machine",
            product_image=SimpleUploadedFile(
                "product.png",
                b"\x89PNG\r\n\x1a\n",
                content_type="image/png",
            ),
            hero_image=SimpleUploadedFile(
                "hero.png",
                b"\x89PNG\r\n\x1a\n",
                content_type="image/png",
            ),
        )
        response = self.client.get(f"/solutions/{machine.slug}/")

        self.assertContains(
            response,
            f"background-image: url('{machine.hero_image.url}');",
        )

    def test_video_embed_url_from_watch_link(self):
        machine = Machine.objects.create(
            model_number="GP-VID-1",
            name="Video Machine",
            video_url="https://youtu.be/j5jGpNVVrUI?si=demo",
        )
        self.assertEqual(
            machine.video_embed_url,
            "https://www.youtube.com/embed/j5jGpNVVrUI",
        )

    def test_solution_detail_renders_video_iframe_from_url(self):
        machine = Machine.objects.create(
            model_number="GP-VID-2",
            name="PDP Video Machine",
            image_path="images/machine1.png",
            features="<ul><li>One</li></ul>",
            video_url="https://youtu.be/j5jGpNVVrUI",
        )
        response = self.client.get(f"/solutions/{machine.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "See It In Action")
        self.assertContains(
            response,
            'src="https://www.youtube.com/embed/j5jGpNVVrUI"',
        )
        self.assertNotContains(response, "youtu.be/j5jGpNVVrUI")

    def test_solution_detail_hides_video_section_when_empty(self):
        machine = Machine.objects.create(
            model_number="GP-VID-3",
            name="No Video Machine",
            image_path="images/machine1.png",
            features="<ul><li>One</li></ul>",
        )
        response = self.client.get(f"/solutions/{machine.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "See It In Action")
