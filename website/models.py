from django.db import models

class Category(models.TextChoices):
    GLUING = "GLUING", "Gluing Machines"
    CARTONING = "CARTONING", "Cartoning Machines"
    CARTONATOR = "CARTONATOR", "Cartonator Machines"
    SHIPPER = "SHIPPER", "Shipper Carton Machines"


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

class Machine(models.Model):
    model_number = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=Category.choices, default=Category.GLUING)
    image_path = models.CharField(max_length=250, help_text="Relative to static folder, e.g., 'images/machine1.png'")
    features = models.JSONField(default=list, help_text="A list of bullet features, e.g., ['Timer base control', 'Auto/Manual system']")
    description = models.TextField(blank=True, default="")
    specifications = models.JSONField(default=dict, blank=True, help_text="Dict of tech specs, e.g., {'speed': '30-60 pcs/min', 'power': '220V'}")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "model_number"]

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
