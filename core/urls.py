from django.urls import path
from core.views import (
    author_list, author_create, author_edit, author_delete, author_detail,
    book_list, book_create, book_edit, book_delete, book_detail,
    review_list, review_create, review_edit, review_delete, review_detail
)

urlpatterns = [
    path("authors/", author_list, name="author_list"),
    path("authors/new/", author_create, name="author_create"),
    path("authors/<author_id>/", author_detail, name="author_detail"),
    path("authors/<author_id>/edit/", author_edit, name="author_edit"),
    path("authors/<author_id>/delete/", author_delete, name="author_delete"),
    path("books/", book_list, name="book_list"),
    path("books/new/", book_create, name="book_create"),
    path("books/<book_id>/", book_detail, name="book_detail"),
    path("books/<book_id>/edit/", book_edit, name="book_edit"),
    path("books/<book_id>/delete/", book_delete, name="book_delete"),
    path("reviews/", review_list, name="review_list"),  
    path("reviews/new/", review_create, name="review_create"),
    path("reviews/<review_id>/", review_detail, name="review_detail"),
    path("reviews/<review_id>/edit/", review_edit, name="review_edit"),
    path("reviews/<review_id>/delete/", review_delete, name="review_delete"),
]