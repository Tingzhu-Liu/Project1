from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("new_page", views.new, name="new"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("search", views.search, name="search"),
    path("random", views.randomPage, name='random')
]
