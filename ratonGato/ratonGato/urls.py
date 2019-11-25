"""ratonGato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

from logic import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('index', views.index, name='landing'),
	path('login_service/', views.login_service, name='login'),
    path('logout_service/', views.logout_service, name='logout'),
    path('signup_service/', views.signup_service, name='signup'),
    path('counter_service/', views.counter_service, name='counter'),
    path('create_game_service/', views.create_game_service, name='create_game'),
    path('join_game_service/', views.join_game_service, name='join_game'),
    path('select_game_service/', views.select_game_service, name='select_game'),
    path('select_game_service/<int:game_id>', views.select_game_service, name='select_game'),
    path('show_game_service/', views.show_game_service, name='show_game'),
    path('move_service/', views.move_service, name='move'),
]
