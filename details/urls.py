from django.urls import path
from .views import *

#Registration of urls
urlpatterns = [
    path('create/', create_project, name="create"),
    path('list/', list_project, name="list"),
    path('update/<int:pk>/', update_project, name="update"),
    path('delete/<int:pk>/', delete_project, name="delete"),
]