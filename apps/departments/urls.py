from django.urls import path
from . import views

urlpatterns = [
    path("", views.department_list, name="department_list"),
    path("add/", views.department_create, name="department_create"),
]
