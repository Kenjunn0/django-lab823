from django.urls import path
from . import views

urlpatterns = [
    path("", views.User.as_view()),
    path("me", views.Me.as_view()),
]