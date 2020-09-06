from django.urls import path

from .views import (
    appointment_create,
    appointment_detail,
    appointment_send_mail,
    appointments_list,
    appointment_delete,
    appointment_update,
)

app_name = "appointments"
urlpatterns = [
    path("", appointments_list, name="appointment-list"),
    path("cadastrar/<int:pet_pk>/", appointment_create, name="appointment-create"),
    path("<int:pk>/", appointment_detail, name="appointment-detail"),
    path("<int:pk>/enviar/email", appointment_send_mail, name="appointment-send-mail"),
    path("<int:pk>/remover/", appointment_delete, name="appointment-delete"),
    path("<int:pk>/editar/", appointment_update, name="appointment-update"),
]
