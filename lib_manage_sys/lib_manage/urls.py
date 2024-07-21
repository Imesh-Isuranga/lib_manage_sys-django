from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginView,name="home"),
    path("register", views.registerView,name="register"),
]
