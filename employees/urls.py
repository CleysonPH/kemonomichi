from django.urls import path

from .views import employee_list, profile


app_name = "employees"
urlpatterns = [
    path("", employee_list, name="employee-list"),
    path("perfil/", profile, name="profile"),
]
