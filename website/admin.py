from django.contrib import admin
from .models import Machine, Testimonial, ContactInquiry

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("model_number", "name", "category", "order")
    list_filter = ("category",)
    search_fields = ("model_number", "name", "description")
    ordering = ("order", "model_number")

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "rating", "order")
    search_fields = ("name", "company", "quote")
    ordering = ("order",)

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "company", "machine_interest", "created_at")
    search_fields = ("name", "email", "company", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)

