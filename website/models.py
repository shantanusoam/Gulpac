from django.db import models

class Category(models.TextChoices):
    GLUING = "GLUING", "Gluing Machines"
    CARTONING = "CARTONING", "Cartoning Machines"
    CARTONATOR = "CARTONATOR", "Cartonator Machines"
    SHIPPER = "SHIPPER", "Shipper Carton Machines"

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

