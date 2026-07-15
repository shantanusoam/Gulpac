from django.shortcuts import render, get_object_or_404, redirect
from django.templatetags.static import static
from django.contrib import messages
from .models import (
    HeroSection,
    MissionVisionSection,
    CardGridSection,
    CTASection,
    ContactInquiry,
    ContactMapSection,
    ContactSection,
    Industry,
    Machine,
    ProductCategory,
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
        "title": defaults.get("title", ""),
        "description": defaults["description"],
        "back_link_label": defaults.get("back_link_label", "Back to Home"),
        "back_link_url": defaults.get("back_link_url", "/"),
        "background_image_url": defaults["background_image_url"],
    }
    context.update({key: value for key, value in defaults.items() if key not in context})
    context.setdefault("show_back_link", True)
    return context


def build_mission_vision_context(page_key, defaults):
    section = MissionVisionSection.objects.filter(page_key=page_key, is_active=True).first()
    if section:
        return {
            "page_key": page_key,
            "mission_title": section.mission_title,
            "mission_description": section.mission_description,
            "vision_title": section.vision_title,
            "vision_description": section.vision_description,
        }

    return {
        "page_key": page_key,
        "mission_title": defaults["mission_title"],
        "mission_description": defaults["mission_description"],
        "vision_title": defaults["vision_title"],
        "vision_description": defaults["vision_description"],
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


def build_industries_context(*, home_only=False):
    industries_qs = Industry.objects.filter(is_active=True)
    if home_only:
        industries_qs = industries_qs.filter(show_on_home=True)

    cards = [
        {
            "title": industry.title,
            "image_url": industry.image.url,
            "detail_image_url": industry.detail_image.url if industry.detail_image else "",
            "bullet_points": industry.bullet_points,
        }
        for industry in industries_qs
    ]
    return {"cards": cards}


def get_industry_grid_defaults():
    return [
        {
            "title": "Food Industry",
            "image_url": static("images/industries/food.jpg"),
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
            "image_url": static("images/industries/pharma.jpg"),
            "bullet_points": [
                "Soap & Toothpaste Boxes",
                "Vials, Ointments",
                "Tubes Boxes",
                "Medical Packaging",
            ],
        },
        {
            "title": "Cosmetics Industry",
            "image_url": static("images/industries/cosmetics.jpg"),
            "bullet_points": [
                "Beauty Products",
                "Bonding of Foam",
                "Pasting of Mirror on Plastic Components",
            ],
        },
        {
            "title": "Paper Industry",
            "image_url": static("images/industries/paper.jpg"),
            "bullet_points": [
                "Tissue Paper Boxes",
                "Paper Bags",
                "Corrugated Boxes",
                "A4 Paper Reams",
            ],
        },
        {
            "title": "Textile Industry",
            "image_url": static("images/industries/textile.jpg"),
            "bullet_points": [
                "Pasting of Velcro on Fabric",
                "Textile Packaging",
            ],
        },
        {
            "title": "Mattress Industry",
            "image_url": static("images/industries/mattress.jpg"),
            "bullet_points": [
                "Bonding of multiple layers of foam in a mattress",
                "Foam Assembly",
            ],
        },
        {
            "title": "Wire Industry",
            "image_url": static("images/industries/wire.jpg"),
            "bullet_points": [
                "Wire Coil Boxes",
                "Cable Packaging",
            ],
        },
        {
            "title": "Automobile Industry",
            "image_url": static("images/industries/automobile.jpg"),
            "bullet_points": [
                "Air Filters",
                "Head Lights",
                "Automotive Parts Packaging",
            ],
        },
    ]


def build_industry_grid_context(*, home_only=False):
    context = build_industries_context(home_only=home_only)
    cards = context["cards"] or get_industry_grid_defaults()
    return {
        "page_key": "industries",
        "section_key": "industries-grid",
        "title": "",
        "description": "",
        "cards": cards,
    }


def build_machine_hero_context(machine):
    return {
        "page_key": f"solutions:{machine.slug}",
        "title": machine.meta_title or machine.name,
        "description": machine.meta_description or machine.description_plain,
        "background_image_url": machine.image_url or static("images/hero/hero-machine.png"),
        "back_link_label": "Back to Home",
        "back_link_url": "/",
        "show_back_link": True,
        "badge_label": f"Model: {machine.model_number}",
        "badge_url": "",
        "centered": False,
    }

def home(request):
    if request.method == "POST":
        ContactInquiry.objects.create(
            name=request.POST.get("name", ""),
            email=request.POST.get("email", ""),
            phone=request.POST.get("phone", ""),
            company=request.POST.get("company", ""),
            message=request.POST.get("message", ""),
        )
        messages.success(request, "Thank you! We'll get back to you within 10 minutes.")
        return redirect("/")

    hero = build_hero_context("home", {
        "title": "Packaging Machines Built For Your Product",
        "description": "Advanced packaging solutions built for speed, precision, and reliability. Empower your production. Elevate your brand.",
        "badge_label": "Precision Bonding, Seamless Packaging",
        "background_image_url": static("images/hero/hero-machine.png"),
        "show_back_link": False,
    })
    machines = Machine.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:3]
    industries = Industry.objects.filter(is_active=True, show_on_home=True)
    return render(request, "website/home.html", {
        "hero": hero,
        "machines": machines,
        "testimonials": testimonials,
        "industries": industries,
    })

def about(request):
    about_hero = build_hero_context("about", {
        "title": "About Us",
        "description": "Discover the engineering story behind Gulpac and the systems we build for safer, cleaner, and more efficient packaging.",
        "background_image_url": static("images/hero/hero-bg.png"),
        "show_back_link": True,
        "back_link_label": "Back to Home",
        "back_link_url": "/",
    })
    mission_vision = build_mission_vision_context("about", {
        "mission_title": "Our Mission",
        "mission_description": (
            "<p>To empower global industries with state-of-the-art, customized gluing and packaging automation. "
            "We commit to continuous technological enhancement, ensuring zero defect rates, high operator safety, "
            "and exceptional long-term machinery value.</p>"
        ),
        "vision_title": "Our Vision",
        "vision_description": (
            "<p>To be internationally recognized as the benchmark of excellence in structural packaging systems. "
            "We strive to pioneer intelligence and PLC capabilities, helping modern manufacturing lines transition "
            "cleanly onto green, low-waste automated solutions.</p>"
        ),
    })
    cta_section = build_cta_context("about", "factory-demo-cta", {
        "heading_prefix": "WANT TO SEE OUR",
        "heading_accent": "FACTORY SETUP?",
        "description": (
            "Let us schedule an in-person workshop visit, or run your dummy cartons on our "
            "demonstration lines over a high-resolution zoom video call."
        ),
        "background_image_url": static("images/about/section-cta-bg.png"),
        "button_label": "Book Demonstration",
        "button_url": "/contact/",
    })
    return render(request, "website/about.html", {
        "about_hero": about_hero,
        "mission_vision": mission_vision,
        "cta_section": cta_section,
    })

def industries(request):
    hero = build_hero_context("industries", {
        "title": "Industries We Serve",
        "description": "Customized packaging solutions engineered for diverse sectors worldwide. From food to pharmaceuticals, cosmetics to automotive - we deliver precision gluing and packaging machines tailored to your industry needs.",
        "back_link_label": "Back to Home",
        "back_link_url": "/",
        "background_image_url": static("images/factory.png"),
    })
    industry_grid = build_industry_grid_context()
    cta_section = build_cta_context("industries", "industries-cta", {
        "heading_prefix": "DON'T SEE YOUR",
        "heading_accent": "INDUSTRY LISTED?",
        "description": "We specialize in custom solutions. Contact us to discuss your specific packaging requirements.",
        "background_image_url": static("images/industries/footer-industry-cta-bg.png"),
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
        "title_prefix": "GET IN",
        "title_accent": "TOUCH",
        "description": "We'd love to hear from you",
        "background_image_url": static("images/contact/inqueryherobg.png"),
        "centered": True,
        "light": True,
        "show_back_link": False,
        "button_label": "Send Message",
        "button_url": "#contact-form",
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
    machines = Machine.objects.select_related("category").all()
    if category_filter:
        machines = machines.filter(category__code=category_filter)

    categories = [
        (category.code, category.name)
        for category in ProductCategory.objects.filter(is_active=True)
    ]
    if not categories:
        categories = list(Category.choices)

    return render(request, "website/solutions.html", {
        "machines": machines,
        "category_filter": category_filter,
        "categories": categories,
    })

def solution_detail(request, slug):
    machine = get_object_or_404(Machine.objects.select_related("category"), slug=slug)
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
    related_machines = Machine.objects.none()
    if machine.category_id:
        related_machines = Machine.objects.filter(category=machine.category).exclude(
            model_number=machine.model_number
        )[:3]
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
