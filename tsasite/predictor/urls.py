from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path("agent", views.agent, name="agent"),
    path("auth", views.auth, name="auth"),
    path("results", views.results, name="results")
]
