from django.contrib import admin
from django.urls import path
from UserPage import views
from .views import Search_User

urlpatterns = [
    path('', views.userHome,name="userhome"),
    path('post/', views.post,name="post"),
    path('delete/<int:postId>', views.postDelete,name="delpost"),
    path('<str:username>', views.userProfile,name="userprofile"),
    path('like_dislike/', views.likePost,name="like_dislike_post"),
    path('slug/comment/', views.comment,name="comment"),
    path('user/follow/<str:username>', views.follow,name="follow"),
    path('search/', Search_User.as_view() ,name="search_user"),
]
