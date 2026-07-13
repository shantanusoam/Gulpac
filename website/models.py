import re

from django.db import models
from django.urls import reverse
from django.utils.html import strip_tags
from django.utils.text import slugify


class Category(models.TextChoices):
    """Legacy category codes kept for seed data and URL filters."""

    GLUING = "GLUING", "Gluing Machines"
    CARTONING = "CARTONING", "Cartoning Machines"
    CARTONATOR = "CARTONATOR", "Cartonator Machines"
    SHIPPER = "SHIPPER", "Shipper Carton Machines"


class ProductType(models.TextChoices):
    NOT_CATEGORIZED = "not_categorized", "Not Categorized"
    STANDARD = "standard", "Standard"
    CUSTOM = "custom", "Custom"


class ProductCategory(models.Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Product category"
        verbose_name_plural = "Product categories"

    def __str__(self):
        return self.name


class PageKey(models.TextChoices):
    HOME = "home", "Home"
    ABOUT = "about", "About"
    INDUSTRIES = "industries", "Industries"
    CONTACT = "contact", "Contact"


class HeroSection(models.Model):
    page_key = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    background_image = models.ImageField(upload_to="hero_sections/", blank=True, null=True)
    back_link_label = models.CharField(max_length=100, default="Back to Home")
    back_link_url = models.CharField(max_length=255, default="/")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.page_key


class MissionVisionSection(models.Model):
    page_key = models.CharField(max_length=100, unique=True, default="about")
    mission_title = models.CharField(max_length=200, default="Our Mission")
    mission_description = models.TextField(
        default=(
            "To empower global industries with state-of-the-art, customized gluing and packaging automation. "
            "We commit to continuous technological enhancement, ensuring zero defect rates, high operator safety, "
            "and exceptional long-term machinery value."
        ),
        help_text="Supports HTML entered through the TinyMCE admin editor.",
    )
    vision_title = models.CharField(max_length=200, default="Our Vision")
    vision_description = models.TextField(
        default=(
            "To be internationally recognized as the benchmark of excellence in structural packaging systems. "
            "We strive to pioneer intelligence and PLC capabilities, helping modern manufacturing lines transition "
            "cleanly onto green, low-waste automated solutions."
        ),
        help_text="Supports HTML entered through the TinyMCE admin editor.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Mission & Vision Section"
        verbose_name_plural = "Mission & Vision Sections"

    def __str__(self):
        return self.page_key


class CardGridSection(models.Model):
    page_key = models.CharField(max_length=100)
    section_key = models.CharField(max_length=100)
    title = models.CharField(max_length=200, blank=True, default="")
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Card Grid Section"
        verbose_name_plural = "Card Grid Sections"
        constraints = [
            models.UniqueConstraint(fields=["page_key", "section_key"], name="unique_card_grid_section")
        ]

    def __str__(self):
        return f"{self.page_key}:{self.section_key}"


class CardGridItem(models.Model):
    section = models.ForeignKey(CardGridSection, related_name="cards", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="card_grid/")
    bullet_points = models.JSONField(default=list)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Industry(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="industries/")
    detail_image = models.ImageField(
        upload_to="industries/",
        blank=True,
        null=True,
        help_text="Optional overlay image for the home page carousel.",
    )
    bullet_points = models.JSONField(default=list)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    show_on_home = models.BooleanField(
        default=True,
        help_text="Show this industry in the home page carousel.",
    )

    class Meta:
        ordering = ["order", "title"]
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.title


class CTASection(models.Model):
    page_key = models.CharField(max_length=100)
    section_key = models.CharField(max_length=100)
    heading_prefix = models.CharField(max_length=200)
    heading_accent = models.CharField(max_length=200)
    description = models.TextField()
    background_image = models.ImageField(upload_to="cta_sections/", blank=True, null=True)
    button_label = models.CharField(max_length=100)
    button_url = models.CharField(max_length=255, default="/contact/")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "CTA Section"
        verbose_name_plural = "CTA Sections"
        constraints = [
            models.UniqueConstraint(fields=["page_key", "section_key"], name="unique_cta_section")
        ]

    def __str__(self):
        return f"{self.page_key}:{self.section_key}"


class ContactSection(models.Model):
    page_key = models.CharField(max_length=100, unique=True)
    intro_prefix = models.CharField(max_length=100, default="GET IN")
    intro_accent = models.CharField(max_length=100, default="TOUCH")
    intro_description = models.CharField(max_length=255, default="We'd love to hear from you")
    form_title = models.CharField(max_length=200, default="Send us a message")
    name_label = models.CharField(max_length=100, default="Name")
    name_placeholder = models.CharField(max_length=100, default="Your name")
    email_label = models.CharField(max_length=100, default="Email")
    email_placeholder = models.CharField(max_length=100, default="your@email.com")
    phone_label = models.CharField(max_length=100, default="Phone")
    phone_placeholder = models.CharField(max_length=100, default="+91 00000 00000")
    message_label = models.CharField(max_length=100, default="Message")
    message_placeholder = models.CharField(max_length=255, default="Tell us about your requirements...")
    button_label = models.CharField(max_length=100, default="Send Message")

    address_title = models.CharField(max_length=100, default="Address")
    address_line1 = models.CharField(max_length=200, default="B5/9, 1st Floor, Paschim Vihar")
    address_line2 = models.CharField(max_length=200, default="New Delhi-110063")
    phone_card_title = models.CharField(max_length=100, default="Phone")
    phone_card_value = models.CharField(max_length=50, default="+91 97173 33206")
    phone_card_href = models.CharField(max_length=100, default="tel:+919717333206")
    email_card_title = models.CharField(max_length=100, default="Email")
    email_card_value = models.CharField(max_length=100, default="contact@glupac.in")
    email_card_href = models.CharField(max_length=100, default="mailto:contact@glupac.in")

    class Meta:
        verbose_name = "Contact Section"
        verbose_name_plural = "Contact Sections"

    def __str__(self):
        return self.page_key


class ContactMapSection(models.Model):
    page_key = models.CharField(max_length=100, unique=True)
    title_prefix = models.CharField(max_length=100, default="Visit Our")
    title_accent = models.CharField(max_length=100, default="Office")
    description = models.CharField(max_length=255, default="Find us on the map")
    map_image = models.ImageField(upload_to="contact_maps/", blank=True, null=True)
    map_image_url = models.URLField(blank=True, default="")

    class Meta:
        verbose_name = "Contact Map Section"
        verbose_name_plural = "Contact Map Sections"

    def __str__(self):
        return self.page_key

class Machine(models.Model):
    model_number = models.CharField(
        "Product SKU ID",
        max_length=50,
        primary_key=True,
    )
    name = models.CharField(max_length=200)
    description = models.TextField(
        blank=True,
        default="",
        help_text="Supports HTML entered through the TinyMCE admin editor.",
    )
    specifications = models.TextField(
        blank=True,
        default="",
        help_text="Supports HTML entered through the TinyMCE admin editor.",
    )
    features = models.TextField(
        blank=True,
        default="",
        help_text="Supports HTML entered through the TinyMCE admin editor.",
    )
    category = models.ForeignKey(
        ProductCategory,
        related_name="products",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    product_image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        help_text="Primary product image shown on listing and detail pages.",
    )
    image_path = models.CharField(
        max_length=250,
        blank=True,
        default="",
        help_text="Legacy static path fallback, e.g., 'images/machine1.png'. Prefer Product image upload.",
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    meta_description = models.TextField(blank=True, default="")
    meta_title = models.CharField(max_length=200, blank=True, default="")
    product_type = models.CharField(
        max_length=50,
        choices=ProductType.choices,
        default=ProductType.NOT_CATEGORIZED,
    )
    brochure = models.FileField(
        upload_to="brochure/",
        blank=True,
        null=True,
        help_text="Optional PDF brochure for this product.",
    )
    video_iframe_html = models.TextField(
        blank=True,
        default="",
        help_text="Optional raw iframe HTML for the PDP video section.",
    )
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "model_number"]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.model_number}-{self.name}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.slug:
            return reverse("solution_detail", kwargs={"slug": self.slug})
        return reverse("solutions")

    @property
    def image_url(self):
        if self.product_image:
            return self.product_image.url
        if self.image_path:
            from django.templatetags.static import static

            return static(self.image_path)
        return ""

    @property
    def description_plain(self):
        return strip_tags(self.description or "").strip()

    @property
    def feature_list(self):
        """Extract plain feature lines from rich-text HTML for card previews."""
        html = self.features or ""
        items = re.findall(r"<li[^>]*>(.*?)</li>", html, flags=re.IGNORECASE | re.DOTALL)
        if items:
            return [strip_tags(item).strip() for item in items if strip_tags(item).strip()]
        text = strip_tags(html)
        return [line.strip("•- \t") for line in text.splitlines() if line.strip()]

    def __str__(self):
        return f"{self.model_number} - {self.name}"

class Testimonial(models.Model):
    name = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    quote = models.TextField()
    rating = models.IntegerField(default=5)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} ({self.company})"

class ContactInquiry(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=150, blank=True, default="")
    message = models.TextField()
    machine_interest = models.CharField(max_length=50, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"Inquiry from {self.name} - {self.company}"
