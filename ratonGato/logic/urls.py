from django.urls import path
from rango import views

app_name='rango'
urlpatterns=[
	path('', views.index, name='index'),
    path('index', views.index, name='index'),

	path('login_service/', views.login_service, name='login_service'),
    path('logout_service/', views.logout_service, name='logout_service'),
    path('signup_service/', views.signup_service, name='signup_service'),
    path('counter_service/', views.counter_service, name='counter_service'),
    path('create_game_service/', views.create_game_service, name='create_game_service'),
    path('join_game_service/', views.join_game_service, name='join_game_service'),
    path('select_game_service/', views.select_game_service, name='select_game_service'),
    path('show_game_service/', views.show_game_service, name='show_game_service'),
    path('move_service/', views.move_service, name='move_service'),
		
]

