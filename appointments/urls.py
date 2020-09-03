from django.urls import path

from .views import appointment_create, appointment_detail


app_name = "appointments"
urlpatterns = [
    path("cadastrar/<int:pet_pk>/", appointment_create, name="appointment-create"),
    path("<int:pk>/", appointment_detail, name="appointment-detail"),
]
