from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("clientes/", include("clients.urls", namespace="clients")),
    path("pets/", include("pets.urls", namespace="pets")),
    path("consultas/", include("appointments.urls", namespace="appointments")),
    path("funcionarios/", include("employees.urls", namespace="employees")),
    path("contas/", include("accounts.urls", namespace="accounts")),
    path("admin/", admin.site.urls),
]
