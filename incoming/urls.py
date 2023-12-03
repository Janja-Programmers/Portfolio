from django.urls import path
from .views import *
#from blog import views 

urlpatterns = [
    path('', home, name="home"),
    path('about/', about, name="about"),
    path('projects/', projects, name="projects"),
    path('blog/', blog, name="blog"),
    path('team/', team, name="team"),
    path('services/', services, name="services"),
    path('contact', contact, name="contact"),
    path('blankpage/', blankpage, name="blankpage"),
    path('send_email/', send_email_view, name='send_email'),
    path('enroll/', enroll, name='enroll')
]