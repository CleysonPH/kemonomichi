from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("clientes/", include("clients.urls", namespace="clients")),
    path("admin/", admin.site.urls),
]
