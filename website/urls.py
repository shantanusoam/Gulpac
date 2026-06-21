from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("industries/", views.industries, name="industries"),
    path("contact/", views.contact, name="contact"),
    path("solutions/", views.solutions, name="solutions"),
    path("solutions/<str:model_number>/", views.solution_detail, name="solution_detail"),
]
