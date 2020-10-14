from django.contrib import admin
from django.urls import path
from UserPage import views

urlpatterns = [
    path('', views.username,name="username"),
    path('post/', views.post,name="post"),
    path('<int:postId>', views.postDelete,name="delpost"),
    path('<str:username>', views.userProfile,name="userprofile"),
]