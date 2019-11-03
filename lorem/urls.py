from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='lorem-home'),
    path('about/', views.about, name='lorem-about'),
]