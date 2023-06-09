from django.urls import path 
from KTCC import views

urlpatterns = [ 
    path('', views.welcome, name='welcome'), 
    path('welcome/', views.welcome, name='welcome'), 
    path('KTCC/', views.KTCC, name='KTCC'),
    path('login/',views.LoginPage,name='login'),
    path('signup/',views.SignupPage,name='signup'), 
    path('logout/',views.LogoutPage,name='logout'),
    path('Teams/', views.Teams, name='Teams'),
    path('Players/', views.Players, name='Players'),
    path('players_regi/', views.players_regi, name='players_regi'),
    path('Table/', views.Table, name='Table'),
    path('Stats/', views.Stats, name='Stats'),
    path('Matches/', views.Matches, name='Matches'),
    path('profile/', views.profile, name='profile'),
    path('Bid_Screen/', views.Bid_Screen, name='Bid_Screen'),
    path('Bid_Screen_new_Player', views.Bid_Screen_new_Player, name='Bid_Screen_new_Player'),
    path('pdf',views.getpdf), 
    path('pdfGen/', views.pdfGen, name='pdfGen'),
    path('BidStatus', views.BidStatus, name='BidStatus'),
    path('Teams/<int:id>',views.Team_players, name='Team_players'), 
    path('Icon_Player',views.Icon_Player, name='Icon_Player'), 

]

handler404= 'KTCC.views.handle_not_found'
