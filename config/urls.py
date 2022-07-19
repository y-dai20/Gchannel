"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import imp
from os import stat
from django.contrib import admin
from django.urls import path
from base import views
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # Account
    path('login/', views.LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('signup/', views.SignUpView.as_view()),
    path('profile/', views.ProfileUpdateView.as_view()),
    path('user/<str:name>/', views.UserDetailView.as_view()),
    # Room
    path('room/<str:pk>/', views.ShowRoomView.as_view()),
    path('join/room/<str:pk>/', views.JoinRoomView.as_view()),
    path('createroom/', views.CreateRoomView.as_view()),
    # Follow
    path('follow/user/<str:name>/', views.FollowView.as_view()),
    path('block/user/<str:name>/', views.BlockView.as_view()),
    # Post
    path('post/', views.PostView.as_view()),
    path('post/<str:pk>/', views.PostDetailView.as_view(), name="post_detail"),
    path('large/post/<str:pk>/', views.LargePostDetailView.as_view()),
    path('post/edit/<str:pk>/', views.PostEditView.as_view()), 
    path('post/delete/<str:pk>/', views.PostDeleteView.as_view()),
    path('post/<str:pk>/reply/', views.ReplyPostView.as_view()),
    path('post/agree/<str:pk>/', views.PostAgreeView.as_view()),
    path('post/disagree/<str:pk>/', views.PostAgreeView.as_view()),
    path('post/favorite/<str:pk>/', views.FavoritePostView.as_view()),
    # Reply
    path('reply/like/<str:pk>/', views.LikeReplyView.as_view()),
    path('reply/<str:pk>/', views.ReplyDetailView.as_view()),
    path('reply/<str:pk>/reply/', views.ReplyReplyView.as_view()),
    # get
    # path('get/reply-type-id/', views.GetReplyTypeIdView.as_view()),
    

    path('', views.IndexListView.as_view()),
    path('large/', views.LargePostIndexListView.as_view()),
    path('favorite/', views.FavoritePostIndexListView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)