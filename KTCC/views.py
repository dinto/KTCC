from django.shortcuts import render,HttpResponse,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreatePlayer
from KTCC.models import PlayerInfo
from .forms import CreateTeam
from KTCC.models import TeamInfo
from KTCC.models import Bid_Bucket
from random import randint
from reportlab.pdfgen import canvas  
from django.http import HttpResponse
from django.http import FileResponse,HttpResponseRedirect
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter 
from django.core.paginator import Paginator
from KTCC.models import VideoLink,CurrentBid,Season,ImportantDate

# Create your views here.

@login_required(login_url='login')
def KTCC(request): 
    Important_Date = ImportantDate.objects.all()
    Videos_models= VideoLink.objects.all().order_by('-id')
    p = Paginator(Videos_models,3)
    page = request.GET.get('page')
    Videos = p.get_page(page)
    nums = "a" * Videos.paginator.num_pages
    return render(request,'index.html',{'ImportantDate':Important_Date,'Videos':Videos,'nums':nums})

def welcome(request): 
    Important_Date = ImportantDate.objects.all()
    Videos_models= VideoLink.objects.all().order_by('-id')
    p = Paginator(Videos_models,3)
    page = request.GET.get('page')
    Videos = p.get_page(page)
    nums = "a" * Videos.paginator.num_pages
    return render(request,'welcome.html',{'ImportantDate':Important_Date,'Videos':Videos,'nums':nums})
    #return render(request,'Teams.html',{})

def Teams(request): 
    Teams= TeamInfo.objects.all()
    return render(request,'Teams.html',{'Teams':Teams})

def Players(request): 
    players= PlayerInfo.objects.all()
    return render(request,'Players.html',{'players':players})

def SignupPage(request):
    if request.method=='POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('KTCC')
    return render (request,'Authentication/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('KTCC')
        else:
           return redirect('login')
           # return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'Authentication/login.html')

def LogoutPage(request):
    logout(request)
    return redirect('login')


def players_regi(request):
   
    if request.method == "POST":
        forms = CreatePlayer(request.POST, request.FILES)

        if forms.is_valid():
            #handle_uploaded_file(request.FILES['Pic_img']) 
            forms.save()
            return redirect("Players")
        #messages.success(request, "Player Registration Successfully!")
        
    else:
        forms = CreatePlayer()
    context = {
        "forms": forms
    }
    return render(request, "registration.html", context)

def Table(request): 
    return render(request,'Table.html',{})

def Stats(request): 
    return render(request,'Stats.html',{})

def Matches(request): 
    return render(request,'Matches.html',{})

@login_required(login_url='login')
def profile(request): 
    if request.method == "POST":
        forms = CreateTeam(request.POST, request.FILES)
        if forms.is_valid():
            forms.instance.Users = request.user
            #check user already create a team
            Team=TeamInfo.objects.filter(Users = request.user)
            if Team:
                print("team already exist")
            else:
                forms.save()
                messages.success(request, 'Team Details Added Successfully')
            return redirect("KTCC")
    
    else:
        forms = CreateTeam()
    context = {
        "forms": forms
    }
    return render(request, "profile.html", context)

@login_required(login_url='login')
def Bid_Screen(request): 
    if request.user.is_authenticated:
        username = request.user.username
    random_object =Bid_Bucket.objects.filter(Current_player = True)
    CurrentBids = CurrentBid.objects.all()
    Base_piont=Season.objects.values('Base_Point_For_Player')[0]['Base_Point_For_Player']
    if request.method == "POST" and 'Increment' in request.POST: 
        current_user = request.user
        if(CurrentBids):
            if(CurrentBids[0].Current_Bid_Point >= Base_piont and CurrentBids[0].Current_Bid_Point<3000):
                incremental=CurrentBids[0].Current_Bid_Point+200
            if(CurrentBids[0].Current_Bid_Point >= 3000 and CurrentBids[0].Current_Bid_Point<10000):
                incremental=CurrentBids[0].Current_Bid_Point+500
            if(CurrentBids[0].Current_Bid_Point >= 10000):
                incremental=CurrentBids[0].Current_Bid_Point+1000
            CurrentBid_details=CurrentBid.objects.filter(Player_name = random_object[0].Player_name)
            current_team =TeamInfo.objects.filter(Users = current_user.id)
            CurrentBid_details.update(Team_Name=current_team[0],Current_Bid_Point=incremental)
        else:
            current_team =TeamInfo.objects.filter(Users = current_user.id)
            CurrentBid_details=CurrentBid.objects.create(
                Player_name=random_object[0].Player_name,
                Current_Bid_Point=Base_piont+200,
                Team_Name=current_team[0],
                Season=random_object[0].Season
            )
            CurrentBid_details.save()
        context = {
            "random_object": random_object,
            "CurrentBid":CurrentBids,
            "username":username
        }
        return render(request, "Bid_Screen.html",context)
    context = {
        "random_object": random_object,
        "CurrentBid":CurrentBids,
        "username":username
    }
    return render(request, "Bid_Screen.html",context)


@login_required(login_url='login')
def Bid_Screen_new_Player(request): 
    Bid_bucket_count=Bid_Bucket.objects.count()
    if(Bid_bucket_count>0):
        current_bid_player_count =Bid_Bucket.objects.filter(Current_player = True).count()
        if(current_bid_player_count>0):
            random_object =Bid_Bucket.objects.filter(Current_player = True)
            context = {
                "random_object": random_object
            }
            return render(request, "Bid_screen_new_player.html",context)
        else:
            random_object_db = Bid_Bucket.objects.all()[randint(0, Bid_bucket_count - 1)] #single random object
            Bid_Bucket.objects.filter(Player_name = random_object_db.Player_name).update(Current_player = True)
            random_object =Bid_Bucket.objects.filter(Current_player = True)
            context = {
            "random_object": random_object
            }
            return render(request, "Bid_screen_new_player.html",context)
    else:
        players= PlayerInfo.objects.all()
        for i in players:
            Bucket=Bid_Bucket.objects.create(Player_name=i,Status='OPEN',Season=i.Season,Current_player=False)
            Bucket.save()
        return render(request, "Bid_screen_new_player.html")

def getpdfs(request):  
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'  
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 55)  
    p.drawString(100,700, "Hello, Javatpoint.")  
    p.showPage()  
    p.save()  
    return response  


def getpdfss(request):
    buf=io.BytesIO()
    c=canvas.Canvas(buf,pagesize=letter,bottomup=0)
    c=canvas.Canvas(response)  
    textob=c.beginText()
    textob.setFont("Helvetica",14)
    players= PlayerInfo.objects.all()
    lines =[]
    for player in players:
        lines.append(player.name)
        lines.append(player.name)
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save
    buf.seek(0)

   # return response 
    return FileResponse(buf,as_attachment=True,filename='ve.pdf')

def getpdf(request):  
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = 'attachment; filename="file.pdf"'  
    p = canvas.Canvas(response)  
    p.setFont("Times-Roman", 55)  
    lines =[]
    players= PlayerInfo.objects.all()
    for player in players:
        lines.append(player.name)
      #  lines.append(player.name)
    for line in lines:
       # textob.textLine(line)
       
        p.drawString(100,700, line)  
    #p.drawString(100,700, "Hello, Javatpoint.")  
    p.showPage()  
    p.save()  
    return response  

def handle_not_found(request, exception):
    print("her")
    return render(request,'handle_not_found.html')