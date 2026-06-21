from django.shortcuts import render, get_object_or_404
from django.templatetags.static import static
from django.contrib import messages
from .models import (
    HeroSection,
    CardGridSection,
    CTASection,
    ContactInquiry,
    ContactMapSection,
    ContactSection,
    Machine,
    Testimonial,
    Category,
)


def build_hero_context(page_key, defaults):
    hero = HeroSection.objects.filter(page_key=page_key, is_active=True).first()
    if hero:
        context = {
            "page_key": hero.page_key,
            "title": hero.title,
            "description": hero.description,
            "back_link_label": hero.back_link_label,
            "back_link_url": hero.back_link_url,
            "background_image_url": hero.background_image.url if hero.background_image else defaults["background_image_url"],
        }
        context.update({key: value for key, value in defaults.items() if key not in context})
        context.setdefault("show_back_link", True)
        return context

    context = {
        "page_key": page_key,
        "title": defaults["title"],
        "description": defaults["description"],
        "back_link_label": defaults.get("back_link_label", "Back to Home"),
        "back_link_url": defaults.get("back_link_url", "/"),
        "background_image_url": defaults["background_image_url"],
    }
    context.update({key: value for key, value in defaults.items() if key not in context})
    context.setdefault("show_back_link", True)
    return context


def build_card_grid_context(page_key, section_key, defaults):
    section = (
        CardGridSection.objects.filter(
            page_key=page_key,
            section_key=section_key,
            is_active=True,
        )
        .prefetch_related("cards")
        .first()
    )
    if section:
        cards = [
            {
                "title": card.title,
                "image_url": card.image.url,
                "bullet_points": card.bullet_points,
            }
            for card in section.cards.filter(is_active=True)
        ]
        if not cards:
            cards = defaults.get("cards", [])
        return {
            "page_key": page_key,
            "section_key": section.section_key,
            "title": section.title,
            "description": section.description,
            "cards": cards,
        }

    return {
        "page_key": page_key,
        "section_key": section_key,
        "title": defaults.get("title", ""),
        "description": defaults.get("description", ""),
        "cards": defaults.get("cards", []),
    }


def build_cta_context(page_key, section_key, defaults):
    cta = CTASection.objects.filter(page_key=page_key, section_key=section_key, is_active=True).first()
    if cta:
        return {
            "page_key": page_key,
            "section_key": section_key,
            "heading_prefix": cta.heading_prefix,
            "heading_accent": cta.heading_accent,
            "description": cta.description,
            "background_image_url": cta.background_image.url if cta.background_image else defaults.get("background_image_url", ""),
            "button_label": cta.button_label,
            "button_url": cta.button_url,
        }

    return {
        "page_key": page_key,
        "section_key": section_key,
        "heading_prefix": defaults["heading_prefix"],
        "heading_accent": defaults["heading_accent"],
        "description": defaults["description"],
        "background_image_url": defaults.get("background_image_url", ""),
        "button_label": defaults["button_label"],
        "button_url": defaults.get("button_url", "/contact/"),
    }


def build_contact_section_context(page_key, defaults):
    section = ContactSection.objects.filter(page_key=page_key).first()
    if section:
        return {
            "page_key": page_key,
            "intro_prefix": section.intro_prefix,
            "intro_accent": section.intro_accent,
            "intro_description": section.intro_description,
            "form_title": section.form_title,
            "name_label": section.name_label,
            "name_placeholder": section.name_placeholder,
            "email_label": section.email_label,
            "email_placeholder": section.email_placeholder,
            "phone_label": section.phone_label,
            "phone_placeholder": section.phone_placeholder,
            "message_label": section.message_label,
            "message_placeholder": section.message_placeholder,
            "button_label": section.button_label,
            "address_title": section.address_title,
            "address_line1": section.address_line1,
            "address_line2": section.address_line2,
            "phone_card_title": section.phone_card_title,
            "phone_card_value": section.phone_card_value,
            "phone_card_href": section.phone_card_href,
            "email_card_title": section.email_card_title,
            "email_card_value": section.email_card_value,
            "email_card_href": section.email_card_href,
        }

    return {
        "page_key": page_key,
        **defaults,
    }


def build_contact_map_context(page_key, defaults):
    section = ContactMapSection.objects.filter(page_key=page_key).first()
    if section:
        return {
            "page_key": page_key,
            "title_prefix": section.title_prefix,
            "title_accent": section.title_accent,
            "description": section.description,
            "image_url": section.map_image.url if section.map_image else (section.map_image_url or defaults["image_url"]),
        }

    return {
        "page_key": page_key,
        **defaults,
    }


def build_machine_hero_context(machine):
    return {
        "page_key": f"solutions:{machine.slug}",
        "title": machine.name,
        "description": machine.description,
        "background_image_url": static(machine.image_path),
        "back_link_label": "Back to Home",
        "back_link_url": "/",
        "show_back_link": True,
        "badge_label": f"Model: {machine.model_number}",
        "badge_url": "",
        "centered": False,
    }

def home(request):
    machines = Machine.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:3]
    return render(request, "website/home.html", {
        "machines": machines,
        "testimonials": testimonials,
    })

def about(request):
    return render(request, "website/about.html")

def industries(request):
    hero = build_hero_context("industries", {
        "title": "Industries We Serve",
        "description": "Customized packaging solutions engineered for diverse sectors worldwide. From food to pharmaceuticals, cosmetics to automotive - we deliver precision gluing and packaging machines tailored to your industry needs.",
        "back_link_label": "Back to Home",
        "back_link_url": "/",
        "background_image_url": static("images/factory.png"),
    })
    industry_grid = build_card_grid_context("industries", "industries-grid", {
        "cards": [
            {
                "title": "Food Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/754aa4a8-77fe-4c35-8c3b-65e43c5bacb7",
                "bullet_points": [
                    "Ready to Eat Food Boxes",
                    "Spice Boxes",
                    "Nuts & Dry Fruit Boxes",
                    "Confectionery Items",
                    "Cereals & Staple Food Boxes",
                    "Sweet Boxes",
                ],
            },
            {
                "title": "Pharma Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/76c67f67-88a6-467d-a93b-5456c594b560",
                "bullet_points": [
                    "Soap & Toothpaste Boxes",
                    "Vials, Ointments",
                    "Tubes Boxes",
                    "Medical Packaging",
                ],
            },
            {
                "title": "Cosmetics Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/1433696f-364c-4a8e-8891-97ee0e001c8b",
                "bullet_points": [
                    "Beauty Products",
                    "Bonding of Foam",
                    "Pasting of Mirror on Plastic Components",
                ],
            },
            {
                "title": "Paper Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/ca412f12-5a0d-460c-971c-c139b558123c",
                "bullet_points": [
                    "Tissue Paper Boxes",
                    "Paper Bags",
                    "Corrugated Boxes",
                    "A4 Paper Reams",
                ],
            },
            {
                "title": "Textile Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/f360d000-e91e-4eb0-b687-bc50a4ecc700",
                "bullet_points": [
                    "Pasting of Velcro on Fabric",
                    "Textile Packaging",
                ],
            },
            {
                "title": "Mattress Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/589d8e7a-4557-4401-8afa-e20c9f2d081b",
                "bullet_points": [
                    "Bonding of multiple layers of foam in a mattress",
                    "Foam Assembly",
                ],
            },
            {
                "title": "Wire Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/61da5c6c-c092-47c0-8148-23a061e9d68a",
                "bullet_points": [
                    "Wire Coil Boxes",
                    "Cable Packaging",
                ],
            },
            {
                "title": "Automobile Industry",
                "image_url": "https://www.figma.com/api/mcp/asset/6ba28cc6-f619-41ac-88d6-4809015449df",
                "bullet_points": [
                    "Air Filters",
                    "Head Lights",
                    "Automotive Parts Packaging",
                ],
            },
        ],
    })
    cta_section = build_cta_context("industries", "industries-cta", {
        "heading_prefix": "DON'T SEE YOUR",
        "heading_accent": "INDUSTRY LISTED?",
        "description": "We specialize in custom solutions. Contact us to discuss your specific packaging requirements.",
        "background_image_url": static("images/component2.png"),
        "button_label": "Contact Us Today",
        "button_url": "/contact/",
    })
    return render(request, "website/industries.html", {
        "hero": hero,
        "industry_grid": industry_grid,
        "cta_section": cta_section,
    })

def contact(request):
    hero = build_hero_context("contact", {
        "title": "Get In Touch",
        "description": "Tell us about your packaging requirement and our team will help you find the right solution.",
        "back_link_label": "Back to Home",
        "back_link_url": "/",
        "background_image_url": static("images/factory.png"),
        "centered": True,
        "show_back_link": False,
        "eyebrow": "Contact Gulpac",
    })
    selected_interest = request.GET.get("interest", "")
    contact_section = build_contact_section_context("contact", {
        "intro_prefix": "GET IN",
        "intro_accent": "TOUCH",
        "intro_description": "We'd love to hear from you",
        "form_title": "Send us a message",
        "name_label": "Name",
        "name_placeholder": "Your name",
        "email_label": "Email",
        "email_placeholder": "your@email.com",
        "phone_label": "Phone",
        "phone_placeholder": "+91 00000 00000",
        "message_label": "Message",
        "message_placeholder": "Tell us about your requirements...",
        "button_label": "Send Message",
        "address_title": "Address",
        "address_line1": "B5/9, 1st Floor, Paschim Vihar",
        "address_line2": "New Delhi-110063",
        "phone_card_title": "Phone",
        "phone_card_value": "+91 97173 33206",
        "phone_card_href": "tel:+919717333206",
        "email_card_title": "Email",
        "email_card_value": "contact@glupac.in",
        "email_card_href": "mailto:contact@glupac.in",
    })
    contact_map = build_contact_map_context("contact", {
        "title_prefix": "Visit Our",
        "title_accent": "Office",
        "description": "Find us on the map",
        "image_url": "https://www.figma.com/api/mcp/asset/95be48c5-54d6-46c5-bd85-e2082beefd35",
    })

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        company = request.POST.get("company", "")
        machine_interest = request.POST.get("machine_interest", selected_interest)
        
        if name and email and phone and message:
            ContactInquiry.objects.create(
                name=name,
                email=email,
                phone=phone,
                company=company,
                message=message,
                machine_interest=machine_interest
            )
            messages.success(request, "Thank you! Your inquiry has been submitted. Our team will contact you shortly.")
        else:
            messages.error(request, "Please fill in all required fields.")

    return render(request, "website/contact.html", {
        "hero": hero,
        "selected_interest": selected_interest,
        "contact_section": contact_section,
        "contact_map": contact_map,
    })

def solutions(request):
    category_filter = request.GET.get("category", "")
    machines = Machine.objects.all()
    if category_filter:
        machines = machines.filter(category=category_filter)
        
    return render(request, "website/solutions.html", {
        "machines": machines,
        "category_filter": category_filter,
        "categories": Category.choices,
    })

def solution_detail(request, slug):
    machine = get_object_or_404(Machine, slug=slug)
    contact_section = build_contact_section_context("contact", {
        "intro_prefix": "INTERESTED IN",
        "intro_accent": "THIS MACHINE?",
        "intro_description": "Send us your requirements and we'll get back to you",
        "form_title": "Send us a message",
        "name_label": "Name",
        "name_placeholder": "Your name",
        "email_label": "Email",
        "email_placeholder": "your@email.com",
        "phone_label": "Phone",
        "phone_placeholder": "+91 00000 00000",
        "message_label": "Message",
        "message_placeholder": "Tell us about your requirements...",
        "button_label": "Send Enquiry",
        "address_title": "Address",
        "address_line1": "B5/9, 1st Floor, Paschim Vihar",
        "address_line2": "New Delhi-110063",
        "phone_card_title": "Phone",
        "phone_card_value": "+91 97173 33206",
        "phone_card_href": "tel:+919717333206",
        "email_card_title": "Email",
        "email_card_value": "contact@glupac.in",
        "email_card_href": "mailto:contact@glupac.in",
    })
    contact_map = build_contact_map_context("contact", {
        "title_prefix": "Visit Our",
        "title_accent": "Office",
        "description": "Find us on the map",
        "image_url": "https://www.figma.com/api/mcp/asset/95be48c5-54d6-46c5-bd85-e2082beefd35",
    })
    # Related machines are other machines in the same category
    related_machines = Machine.objects.filter(category=machine.category).exclude(model_number=machine.model_number)[:3]
    if not related_machines.exists():
        related_machines = Machine.objects.exclude(model_number=machine.model_number)[:3]
        
    return render(request, "website/solution_detail.html", {
        "machine": machine,
        "hero": build_machine_hero_context(machine),
        "contact_section": contact_section,
        "contact_map": contact_map,
        "selected_interest": machine.model_number,
        "related_machines": related_machines,
    })
