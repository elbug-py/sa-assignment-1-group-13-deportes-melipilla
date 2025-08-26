from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("authors/", views.authors_table, name="authors_table"),
    path("authors/new/", views.author_create, name="author_create"),
    path("authors/<author_id>/", views.author_detail, name="author_detail"),
    path("authors/<author_id>/edit/", views.author_edit, name="author_edit"),
    path("authors/<author_id>/delete/", views.author_delete, name="author_delete"),
    path("books/", views.books_table, name="books_table"),
    path("books/new/", views.book_create, name="book_create"),
    path("books/<book_id>/", views.book_detail, name="book_detail"),
    path("books/<book_id>/edit/", views.book_edit, name="book_edit"),
    path("books/<book_id>/delete/", views.book_delete, name="book_delete"),
    path("books/<book_id>/reviews/", views.book_reviews, name="book_reviews"),
    path("books/<book_id>/reviews/new/", views.review_create, name="review_create"),
    path("books/<book_id>/sales/", views.book_sales, name="book_sales"),
    path("books/<book_id>/sales/new/", views.sale_create, name="sale_create"),
    path("top-rated/", views.top_rated, name="top_rated"),
    path("top-selling/", views.top_selling, name="top_selling"),
    path("search/", views.search_books, name="search_books"),
]
