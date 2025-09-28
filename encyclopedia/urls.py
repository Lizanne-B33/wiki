# This file defines the URLs that are used by the application.
# The URL path takes three attributes.  The URL path, what view is called
# when the mapped URL exists, and a name of the URL path which is called by
# the templates to create links to specific views.  They are also used in the
# view code to reverse-resolve URLS (generating a URL from a view name and
# its parameters).

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/", views.index, name="wiki-index"),
    path("wiki/add/", views.add_view, name="wiki-add"),
    path("wiki/random", views.random_view, name="random_view"),
    path("wiki/search/", views.search_view, name="search_view"),
    path("wiki/<str:filename>", views.single_entry_view, name="single_entry"),
    path(
        "wiki/add/<str:filename>", views.single_entry_view, name="added_entry"
    ),
    path("wiki/edit/<str:filename>/", views.edit_view, name="wiki-edit"),
]
