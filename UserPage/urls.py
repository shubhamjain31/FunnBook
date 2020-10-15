from django.contrib import admin
from django.urls import path
from UserPage import views

urlpatterns = [
    path('', views.userHome,name="userhome"),
    path('post/', views.post,name="post"),
    path('delete/<int:postId>', views.postDelete,name="delpost"),
    path('<str:username>', views.userProfile,name="userprofile"),
    path('like_dislike/', views.likePost,name="like_dislike_post"),
]
