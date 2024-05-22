from django.urls import path
from .views import home, create_book, book_inventory, read_and_update_book, borrow_book

app_name = "bookmanagement"

urlpatterns = [
    path("", home, name="home"),
    path("books/create/", create_book, name="create_book"),
    path("books/", book_inventory, name="book_inventory"),
    path("books/read/<str:book_id>/", read_and_update_book, name="read_and_update_book"),
    path("books/borrow/", borrow_book, name="borrow_book"),
]
