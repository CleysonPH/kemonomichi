from django.urls import path

from .views import pet_create, pet_detail, pet_delete


app_name = "pets"
urlpatterns = [
    path("cadastrar/<int:owner_pk>/", pet_create, name="pet-create"),
    path("<int:pk>/detalhes/", pet_detail, name="pet-detail"),
    path("<int:pk>/remover/", pet_delete, name="pet-delete"),
]
