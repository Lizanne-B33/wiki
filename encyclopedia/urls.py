from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki-index"),
    path("wiki/add/", views.add_view, name="wiki-add"),
    path("wiki/edit/", views.edit_view, name="wiki-edit"),
    path("wiki/random", views.random_view, name="random_view"),
    path("wiki/search/", views.search_view, name="search_view"),
    path("wiki/<str:filename>", views.single_entry_view, name="single_entry"),
    path(
        "wiki/add/<str:filename>", views.single_entry_view, name="added_entry"
    ),
]
