from django.urls import path

from .views import (
    client_create,
    client_detail,
    client_list,
    client_update,
    client_delete,
)


app_name = "clients"
urlpatterns = [
    path("", client_list, name="client-list"),
    path("cadastrar/", client_create, name="client-create"),
    path("<int:pk>/detalhes/", client_detail, name="client-detail"),
    path("<int:pk>/editar/", client_update, name="client-update"),
    path("<int:pk>/remover/", client_delete, name="client-delete"),
]
