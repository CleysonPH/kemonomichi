from django.urls import path

from .views import signin, signout


app_name = "accounts"
urlpatterns = [
    path("login", signin, name="signin"),
    path("logout", signout, name="signout"),
]
