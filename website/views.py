from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.contrib import messages
from .models import HeroSection, CardGridSection, CTASection, Machine, Testimonial, ContactInquiry, Category


def build_hero_context(page_key, defaults):
    hero = HeroSection.objects.filter(page_key=page_key, is_active=True).first()
    if hero:
        return {
            "page_key": hero.page_key,
            "title": hero.title,
            "description": hero.description,
            "back_link_label": hero.back_link_label,
            "back_link_url": hero.back_link_url,
            "background_image_url": hero.background_image.url if hero.background_image else defaults["background_image_url"],
        }

    return {
        "page_key": page_key,
        "title": defaults["title"],
        "description": defaults["description"],
        "back_link_label": defaults.get("back_link_label", "Back to Home"),
        "back_link_url": defaults.get("back_link_url", "/"),
        "background_image_url": defaults["background_image_url"],
    }


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
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        company = request.POST.get("company", "")
        message = request.POST.get("message")
        machine_interest = request.POST.get("machine_interest", "")
        
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
            return render(request, "website/contact.html", {"success": True})
        else:
            messages.error(request, "Please fill in all required fields.")
            
    machines = Machine.objects.all()
    return render(request, "website/contact.html", {"machines": machines})

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

def solution_detail(request, model_number):
    machine = get_object_or_404(Machine, model_number=model_number)
    # Related machines are other machines in the same category
    related_machines = Machine.objects.filter(category=machine.category).exclude(model_number=machine.model_number)[:3]
    if not related_machines.exists():
        related_machines = Machine.objects.exclude(model_number=machine.model_number)[:3]
        
    return render(request, "website/solution_detail.html", {
        "machine": machine,
        "related_machines": related_machines,
    })
