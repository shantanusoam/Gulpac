from django.contrib import admin
from .models import (
    CTASection,
    ContactInquiry,
    ContactMapSection,
    ContactSection,
    HeroSection,
    CardGridItem,
    CardGridSection,
    Machine,
    Testimonial,
)


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


@admin.register(ContactSection)
class ContactSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "form_title")
    search_fields = (
        "page_key",
        "intro_prefix",
        "intro_accent",
        "intro_description",
        "form_title",
        "address_line1",
        "address_line2",
        "phone_card_value",
        "email_card_value",
    )


@admin.register(ContactMapSection)
class ContactMapSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "title_prefix", "title_accent")
    search_fields = ("page_key", "title_prefix", "title_accent", "description", "map_image_url")

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("model_number", "slug", "name", "category", "order")
    list_filter = ("category",)
    search_fields = ("model_number", "slug", "name", "description", "video_iframe_html")
    prepopulated_fields = {"slug": ("model_number", "name")}
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
