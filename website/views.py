from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Machine, Testimonial, ContactInquiry, Category

def home(request):
    machines = Machine.objects.all()[:6]
    testimonials = Testimonial.objects.all()[:3]
    return render(request, "website/home.html", {
        "machines": machines,
        "testimonials": testimonials,
    })

def about(request):
    return render(request, "website/about.html")

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

