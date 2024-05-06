from django.urls import path

from . import views, util

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("new/", views.newentry, name="newentry"),
    path("edit/", views.edit, name="edit"),
    path("saveedit", views.saveedit, name="saveedit"),
    path("random/", views.randomchoice, name="randomchoice")
]
