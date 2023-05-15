from django.urls import path 
from KTCC import views

urlpatterns = [ 
    path('', views.welcome, name='welcome'), 
    path('KTCC/', views.KTCC, name='index'),

]
