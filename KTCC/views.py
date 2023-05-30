from django.shortcuts import render,HttpResponse,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreatePlayer
from .forms import CreateTeam
from random import randint
from reportlab.pdfgen import canvas  
from django.http import HttpResponse
from django.http import FileResponse,HttpResponseRedirect
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter 
from django.core.paginator import Paginator
from KTCC.models import VideoLink,CurrentBid,Season,ImportantDate,Available_Point_Table,Bid_Details,Unsold_player,Schedule,TeamInfo,Bid_Bucket,PlayerInfo
from reportlab.platypus import Image

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
    
    matches= Schedule.objects.all()
    return render(request,'Matches.html',{'matches':matches})

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
                current_team =TeamInfo.objects.filter(Users = request.user.id)
                Maximum_Bid_Point=Season.objects.filter(Season_Name=current_team[0].Season)
                Available_Point_Table_details=Available_Point_Table.objects.create(
                Available_Point=Maximum_Bid_Point[0].Maximum_Bid_Point,
                Team_Name=current_team[0],
                Season=current_team[0].Season
                )
                Available_Point_Table_details.save()
                
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
            Available_Point=Available_Point_Table.objects.filter(Team_Name=current_team[0])
            if(Available_Point[0].Available_Point>=incremental):
                CurrentBid_details.update(Team_Name=current_team[0],Current_Bid_Point=incremental)
        else:
            current_team =TeamInfo.objects.filter(Users = current_user.id)
            Available_Point=Available_Point_Table.objects.filter(Team_Name=current_team[0])
            if(Available_Point[0].Available_Point>=1000):
                CurrentBid_details=CurrentBid.objects.create(
                    Player_name=random_object[0].Player_name,
                    Current_Bid_Point=Base_piont,
                    Team_Name=current_team[0],
                    Season=random_object[0].Season
                )
                CurrentBid_details.save()
        context = {
            "random_object": random_object,
            "CurrentBid":CurrentBids,
            "username":username,
            "Base_piont":Base_piont
        }
        return render(request, "Bid_Screen.html",context)
    context = {
        "random_object": random_object,
        "CurrentBid":CurrentBids,
        "username":username,
        "Base_piont":Base_piont
    }
    return render(request, "Bid_Screen.html",context)


@login_required(login_url='login')
def Bid_Screen_new_Player(request): 
    Bid_bucket_count=Bid_Bucket.objects.count()
    if request.method == "POST" and 'StartBid' in request.POST: 
        Bid_bucket_count=Bid_Bucket.objects.count()
        if(Bid_bucket_count<1):
            players= PlayerInfo.objects.all()
            for i in players:
                Bucket=Bid_Bucket.objects.create(Player_name=i,Status='OPEN',Season=i.Season,Current_player=False)
                Bucket.save()
    if request.method == "POST" and 'Sold' in request.POST: 
        CurrentBids = CurrentBid.objects.all()
        if(CurrentBid.objects.count()>0):     
            Bid_Detail=Bid_Details.objects.create(
                Player_name=CurrentBids[0].Player_name,
                Status='Sold',
                Sold_Point=CurrentBids[0].Current_Bid_Point,
                Team_Name=CurrentBids[0].Team_Name,
                Season=CurrentBids[0].Season
                )
            Bid_Detail.save()
            Available_Point=Available_Point_Table.objects.filter(Team_Name=CurrentBids[0].Team_Name)
            new_availablepoint=Available_Point[0].Available_Point-CurrentBids[0].Current_Bid_Point
            Available_Point_Table.objects.filter(Team_Name=CurrentBids[0].Team_Name).update(Available_Point = new_availablepoint)
            CurrentBids.delete()
            Bid_Bucket.objects.filter(Current_player = True).delete()
        
    if request.method == "POST" and 'UnSold' in request.POST: 
        CurrentBids = CurrentBid.objects.all()
        if(CurrentBid.objects.count()<1):  
            print("UnSold")   
            Bid_Bucket_details=Bid_Bucket.objects.filter(Current_player = True)
            Unsold_players=Unsold_player.objects.create(
                Player_name=Bid_Bucket_details[0].Player_name,
                Status='UnSold',
                Season=Bid_Bucket_details[0].Season
                )
            Unsold_players.save()
            CurrentBids.delete()
            Bid_Bucket.objects.filter(Current_player = True).delete()
    if request.method == "POST" and 'REAUCTION' in request.POST:
        Bid_bucket_count=Bid_Bucket.objects.count()
        if(Bid_bucket_count<1):
            players= Unsold_player.objects.all()
            for i in players:
                Bucket=Bid_Bucket.objects.create(Player_name=i.Player_name,Status='REAUCTION',Season=i.Season,Current_player=False)
                Bucket.save()
                instance = Unsold_player.objects.get(Player_name=i.Player_name)
                instance.delete()

    print("Bid_bucket_count",Bid_bucket_count)
    if(Bid_bucket_count>0):
        current_bid_player_count =Bid_Bucket.objects.filter(Current_player = True).count()
        Base_piont=Season.objects.values('Base_Point_For_Player')[0]['Base_Point_For_Player']
        CurrentBids = CurrentBid.objects.all()
        print("current_bid_player_count",current_bid_player_count)
        if(current_bid_player_count>0):
            random_object =Bid_Bucket.objects.filter(Current_player = True)
            context = {
                "random_object": random_object,
                "CurrentBid":CurrentBids,
                "Base_piont":Base_piont
            }
            return render(request, "Bid_screen_new_player.html",context)
        else:
            if request.method == "POST" and 'NewPlayer' in request.POST: 
                print("NewPlayer")
                random_object_db = Bid_Bucket.objects.all()[randint(0, Bid_bucket_count - 1)] #single random object
                Bid_Bucket.objects.filter(Player_name = random_object_db.Player_name).update(Current_player = True)
                random_object =Bid_Bucket.objects.filter(Current_player = True)
                context = {
                "random_object": random_object,
                "CurrentBid":CurrentBids,
                "Base_piont":Base_piont
                }
                return render(request, "Bid_screen_new_player.html",context)
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
    lines.append(Image('static/images/LogoT10.jpeg',2.2*inch,2.2*inch))
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

#def Season_Details(request):
#    return {'Season_Details': Season.objects.all()}
def BidStatus(request):
    Sold_Players = Bid_Details.objects.all()
    context = {
        "Sold_Players":Sold_Players
    }
    return render(request, "BidStatus.html",context)

def Team_players(request,id):
    Team_name=TeamInfo.objects.get(id=id)
    #print(Bid_Details.objects.filter(Team_Name=Team_name.id))
    Team_players = Bid_Details.objects.filter(Team_Name=Team_name.id)
    context = {
        "Team_players":Team_players
    }
    return render(request, "Team_Players.html",context)
def Icon_Player(request):
    #Players = Bid_Details.objects.get()
    #context = {
    #    "Sold_Players":Sold_Players
    #}
    return render(request, "Icon_Player_selection.html")
    