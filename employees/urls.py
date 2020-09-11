from django.urls import path

from .views import employee_list, profile, employee_detail


app_name = "employees"
urlpatterns = [
    path("", employee_list, name="employee-list"),
    path("perfil/", profile, name="profile"),
    path("<str:username>/", employee_detail, name="employee-detail"),
]
