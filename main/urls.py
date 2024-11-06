from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('onboarding', views.onboarding, name='onboarding'),
    path('enroll/', views.learn, name='learn'),
    path('contact/', views.contact, name='contact'),
    path('stk-status/', views.stk_status_view, name='stk_status'),
    path('callback/', views.payment_callback, name='payment_callback'),
]
