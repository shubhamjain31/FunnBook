from django.contrib import admin
from django.urls import path
from . import views

app_name = "story_app"
urlpatterns = [
    path('', views.Home.as_view(),name="userhome"),
]
