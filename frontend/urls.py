from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("authors/", views.authors_table, name="authors_table"),
    path("top-rated/", views.top_rated, name="top_rated"),
    path("top-selling/", views.top_selling, name="top_selling"),
    path("search/", views.search_books, name="search_books"),
]
