from django import forms
from django.contrib import admin

from .admin_mixins import PageSectionAdminMixin
from .admin_widgets import RichTextEditorWidget, StringListField
from .models import (
    CTASection,
    CardGridItem,
    CardGridSection,
    ContactInquiry,
    ContactMapSection,
    ContactSection,
    HeroSection,
    Industry,
    Machine,
    MissionVisionSection,
    Testimonial,
)


class HeroSectionAdminForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = "__all__"


class IndustryAdminForm(forms.ModelForm):
    bullet_points = StringListField(
        required=False,
        help_text="Enter one bullet point per line.",
    )

    class Meta:
        model = Industry
        fields = "__all__"


class CardGridItemInlineForm(forms.ModelForm):
    bullet_points = StringListField(
        required=False,
        help_text="One bullet per line.",
    )

    class Meta:
        model = CardGridItem
        fields = "__all__"


class MachineAdminForm(forms.ModelForm):
    features = StringListField(
        required=False,
        help_text="Enter one feature per line.",
    )

    class Meta:
        model = Machine
        # Reason: Hunny asked for image upload only — hide legacy static path field.
        exclude = ("image_path",)


class MissionVisionSectionAdminForm(forms.ModelForm):
    class Meta:
        model = MissionVisionSection
        fields = "__all__"
        widgets = {
            "mission_description": RichTextEditorWidget(),
            "vision_description": RichTextEditorWidget(),
        }


@admin.register(HeroSection)
class HeroSectionAdmin(PageSectionAdminMixin, admin.ModelAdmin):
    form = HeroSectionAdminForm
    list_display = ("page_key", "title", "is_active")
    list_filter = ("page_key", "is_active")
    search_fields = ("page_key", "title", "description")
    fieldsets = (
        (None, {"fields": ("title", "description", "background_image", "is_active")}),
        ("Back link", {"fields": ("back_link_label", "back_link_url")}),
    )


@admin.register(MissionVisionSection)
class MissionVisionSectionAdmin(PageSectionAdminMixin, admin.ModelAdmin):
    form = MissionVisionSectionAdminForm
    list_display = ("page_key", "mission_title", "vision_title", "is_active")
    list_filter = ("page_key", "is_active")
    search_fields = ("page_key", "mission_title", "mission_description", "vision_title", "vision_description")
    fieldsets = (
        ("Mission", {"fields": ("mission_title", "mission_description")}),
        ("Vision", {"fields": ("vision_title", "vision_description")}),
        ("Visibility", {"fields": ("is_active",)}),
    )


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    form = IndustryAdminForm
    list_display = ("title", "order", "is_active", "show_on_home")
    list_filter = ("is_active", "show_on_home")
    search_fields = ("title",)
    ordering = ("order", "title")
    fieldsets = (
        ("Basic info", {"fields": ("title", "order")}),
        ("Images", {"fields": ("image", "detail_image")}),
        ("Bullet points", {"fields": ("bullet_points",)}),
        ("Visibility", {"fields": ("is_active", "show_on_home")}),
    )


class CardGridItemInline(admin.TabularInline):
    model = CardGridItem
    form = CardGridItemInlineForm
    extra = 0


@admin.register(CardGridSection)
class CardGridSectionAdmin(admin.ModelAdmin):
    list_display = ("page_key", "section_key", "title", "is_active")
    list_filter = ("is_active", "page_key")
    search_fields = ("page_key", "section_key", "title", "description")
    inlines = [CardGridItemInline]


@admin.register(CTASection)
class CTASectionAdmin(PageSectionAdminMixin, admin.ModelAdmin):
    list_display = ("page_key", "section_key", "heading_prefix", "heading_accent", "is_active")
    list_filter = ("page_key", "is_active")
    search_fields = ("page_key", "section_key", "heading_prefix", "heading_accent", "description")
    fieldsets = (
        (None, {"fields": ("section_key", "heading_prefix", "heading_accent", "description")}),
        ("Call to action", {"fields": ("button_label", "button_url", "background_image")}),
        ("Visibility", {"fields": ("is_active",)}),
    )


@admin.register(ContactSection)
class ContactSectionAdmin(PageSectionAdminMixin, admin.ModelAdmin):
    list_display = ("page_key", "form_title")
    list_filter = ("page_key",)
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
    fieldsets = (
        ("Intro", {"fields": ("intro_prefix", "intro_accent", "intro_description")}),
        ("Form labels", {"fields": (
            "form_title",
            "name_label", "name_placeholder",
            "email_label", "email_placeholder",
            "phone_label", "phone_placeholder",
            "message_label", "message_placeholder",
            "button_label",
        )}),
        ("Contact cards", {"fields": (
            "address_title", "address_line1", "address_line2",
            "phone_card_title", "phone_card_value", "phone_card_href",
            "email_card_title", "email_card_value", "email_card_href",
        )}),
    )


@admin.register(ContactMapSection)
class ContactMapSectionAdmin(PageSectionAdminMixin, admin.ModelAdmin):
    list_display = ("page_key", "title_prefix", "title_accent")
    list_filter = ("page_key",)
    search_fields = ("page_key", "title_prefix", "title_accent", "description", "map_image_url")
    fieldsets = (
        (None, {"fields": ("title_prefix", "title_accent", "description")}),
        ("Map image", {"fields": ("map_image", "map_image_url")}),
    )


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    form = MachineAdminForm
    list_display = ("model_number", "slug", "name", "category", "order")
    list_filter = ("category",)
    search_fields = ("model_number", "slug", "name", "description", "video_url")
    prepopulated_fields = {"slug": ("model_number", "name")}
    ordering = ("order", "model_number")
    fieldsets = (
        (None, {"fields": ("model_number", "slug", "name", "category")}),
        ("Display & media", {"fields": ("image", "video_url", "order")}),
        ("Content", {"fields": ("description", "features", "specifications")}),
    )


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
