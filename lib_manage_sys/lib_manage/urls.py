from django.urls import path
from . import views

urlpatterns = [
    path("", views.loginView, name="home"),
    path("register/", views.registerView, name="register"),
    path("addBook/", views.addBookView, name="addBook"),
    path("search/", views.searchBook, name="search"),
    path("delete-book/<int:id>/", views.deleteBook, name="delete-book"),
    path("update-book/<int:id>/", views.updateBook, name="update-book"),
    path("update-book-confirm/", views.updateBookConfirm, name="update-book-confirm"),
    path("user-reg/", views.user_reg, name="user-reg"),
]
