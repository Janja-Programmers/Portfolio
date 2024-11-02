from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('enroll/', views.learn, name='learn'),
    path('contact/', views.contact, name='contact'),
]
