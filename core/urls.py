from django.urls import path
from core.views import author_list, author_create, author_edit, author_delete

urlpatterns = [
    path("authors/", author_list, name="author_list"),
    path("authors/", author_create, name="author_create"),
    path("authors/<author_id>/", author_edit, name="author_edit"),
    path("authors/<author_id>/", author_delete, name="author_delete"),
]