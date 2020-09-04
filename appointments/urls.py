from django.urls import path

from .views import appointment_create, appointment_detail, appointment_send_mail


app_name = "appointments"
urlpatterns = [
    path("cadastrar/<int:pet_pk>/", appointment_create, name="appointment-create"),
    path("<int:pk>/", appointment_detail, name="appointment-detail"),
    path("<int:pk>/enviar/email", appointment_send_mail, name="appointment-send-mail"),
]
