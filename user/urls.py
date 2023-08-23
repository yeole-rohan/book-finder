from django.urls import path, include
from . import views
from django.contrib.auth.views import (
    LogoutView, PasswordResetConfirmView, PasswordResetCompleteView
)
urlpatterns = [
    path("", views.profile, name="profile"),
    path("login/", views.shopLogin, name="shopLogin"),
    path("register/", views.register, name="register"),
    path('logout/', LogoutView.as_view(next_page='/'),name='logout'),
]