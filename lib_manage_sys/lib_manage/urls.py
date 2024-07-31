from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginView, name="home"),
    path("register/", views.registerView, name="register"),
    path("addBook/", views.addBookView, name="addBook"),
    path("addBook/<int:id>/", views.addBookView, name="addBook"),
    path("search/", views.searchBook, name="search"),
    path("delete-book/<int:id>/", views.deleteBook, name="delete-book"),
    path("user-reg/", views.user_reg, name="user-reg"),
    path("get-book/", views.getBook, name="get-book"),
    path("handover-book/", views.handover, name="handover"),
    path("handover-delete/", views.handoverDelete, name="handover-delete"),
    path("send-email/", views.send_email, name="send-email"),
    path("filter/<str:category>/", views.filter, name="filter")
]
