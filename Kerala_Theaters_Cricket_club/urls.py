"""Kerala_Theaters_Cricket_club URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from KTCC import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('KTCC.urls')),
    path('home/',views.KTCC,name='home'),
    path('login/',views.LoginPage,name='login'),
    path('signup/',views.SignupPage,name='signup'), 
    path('logout/',views.LogoutPage,name='logout'),
]

  
admin.site.site_header = 'KERALA THEATERS CRICKET CLUB Administration dashboard'                   
admin.site.index_title = 'KERALA THEATERS CRICKET CLUB(KTCC)'                 
admin.site.site_title = 'KERALA THEATERS CRICKET CLUB Administration'