from django.urls import path
from django.contrib import admin

from . import views

urlpatterns = [
    path("", views.user, name="user"),
    path("simulator", views.simulator, name="simulator"),
    path("auth/", views.auth, name="auth"),
    path("results", views.results, name="results")
]
