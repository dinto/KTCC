from django.urls import path 
from KTCC import views

urlpatterns = [ 
    path('welcome/', views.welcome, name='welcome'), 
    path('KTCC/', views.KTCC, name='index'),
    path('Teams/', views.Teams, name='Teams'),
    path('Players/', views.Players, name='Players'),
    path('players_regi/', views.players_regi, name='players_regi'),

]
