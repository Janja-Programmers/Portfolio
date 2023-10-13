from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('services/', services, name="services"),
    path('projects/', projects, name="projects"),
    path('blog/', blog, name="blog"),
    path('team/', team, name="team"),
    path('testimonial/', testimonial, name="testimonial"),
    path('contact', contact, name="contact"),
    path('blankpage/', blankpage, name="blankpage"),
    
]