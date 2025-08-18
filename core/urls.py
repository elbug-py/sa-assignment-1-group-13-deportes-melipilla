from django.urls import path
from core.views import (
    author_list, author_create, author_edit, author_delete,
    book_list, book_create, book_edit, book_delete,
    review_list, review_create, review_edit, review_delete
)

urlpatterns = [
    path("authors/", author_list, name="author_list"),
    path("authors/", author_create, name="author_create"),
    path("authors/<author_id>/", author_edit, name="author_edit"),
    path("authors/<author_id>/", author_delete, name="author_delete"),
    path("books/", book_list, name="book_list"),
    path("books/", book_create, name="book_create"),
    path("books/<book_id>/", book_edit, name="book_edit"),
    path("books/<book_id>/", book_delete, name="book_delete"),
    path("reviews/", review_list, name="review_list"),
    path("reviews/", review_create, name="review_create"),
    path("reviews/<review_id>/", review_edit, name="review_edit"),
    path("reviews/<review_id>/", review_delete, name="review_delete"),
]