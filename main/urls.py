from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('onboarding', views.onboarding, name='onboarding'),
    path('enroll/', views.learn, name='learn'),
    path('contact/', views.contact, name='contact'),
    path('stk-status/', views.stk_status_view, name='stk_status'),
    path('callback/', views.payment_callback, name='payment_callback'),
    path('service/web-development/', views.web_development_detail, name='web-development-detail'),
    path('service/mobile-app-development/', views.mobile_app_development_detail, name='mobile-app-development-detail'),
    path('service/management-information-systems/', views.management_information_systems_detail, name='management-information-systems-detail'),
    path('service/ai-ml-development/', views.ai_ml_development_detail, name='ai-ml-development-detail'),
    path('service/it-consultancy/', views.it_consultancy_detail, name='it-consultancy-detail'),
    path('service/search-engine-optimization/', views.search_engine_optimization_detail, name='search-engine-optimization-detail'),
]
