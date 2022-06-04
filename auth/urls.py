from django.urls import path
from . import api

urlpatterns = [
    path("login/", api.login_callback, name="login"),
    path("register/", api.register_callback, name="register"),
]

