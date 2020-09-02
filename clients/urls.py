from django.urls import path

from .views import client_create, client_detail, client_list


app_name = "clients"
urlpatterns = [
    path("", client_list, name="client-list"),
    path("cadastrar/", client_create, name="client-create"),
    path("<int:pk>/detalhes/", client_detail, name="client-detail"),
]
