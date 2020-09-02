from django.urls import path

from .views import client_create


app_name = "clients"
urlpatterns = [
    path("cadastrar/", client_create, name="client-create"),
]
