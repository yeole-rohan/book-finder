from django.urls import path, include
from . import views
urlpatterns = [
    path("", views.search, name="search"),
    path("add/books/", views.adminsearch, name="adminsearch"),
    path("select-books/", views.selectbooks, name="selectbooks"),
    path("shop/books/", views.shopbooks, name="shopbooks"),
]