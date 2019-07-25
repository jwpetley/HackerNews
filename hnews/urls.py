"""hnews URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from hnews.posts import views as posts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('posts/', include('hnews.posts.urls')),
    path('accounts/login/',
    auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/',
    auth_views.LogoutView.as_view(), name='logout'),
    path('comments/<int:comment_id>/set_upvoted/',
        posts_views.set_upvoted_comment, name='set_upvoted_comment'),
    path('comments/<int:comment_id>/reply/',
        posts_views.add_reply, name='add_reply'),
]
