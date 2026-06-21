from django.contrib import admin
from .models import CTASection, HeroSection, CardGridItem, CardGridSection, Machine, Testimonial, ContactInquiry


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "title", "is_active")
    list_filter = ("is_active",)
    search_fields = ("page_key", "title", "description")


class CardGridItemInline(admin.TabularInline):
    model = CardGridItem
    extra = 0


@admin.register(CardGridSection)
class CardGridSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "section_key", "title", "is_active")
    list_filter = ("is_active", "page_key")
    search_fields = ("page_key", "section_key", "title", "description")
    inlines = [CardGridItemInline]


@admin.register(CTASection)
class CTASectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "section_key", "heading_prefix", "heading_accent", "is_active")
    list_filter = ("is_active", "page_key")
    search_fields = ("page_key", "section_key", "heading_prefix", "heading_accent", "description")

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
