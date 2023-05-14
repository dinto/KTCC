from django.urls import path 
from KTCC import views

urlpatterns = [ 
    path('', views.KTCC, name='index'), 
]
