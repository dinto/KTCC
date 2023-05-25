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
from django.http import FileResponse
import io
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from KTCC.models import ImportantDate

# Create your views here.

@login_required(login_url='login')
def KTCC(request): 
    return render(request,'index.html',{})

def welcome(request): 
    Important_Date = ImportantDate.objects.all()
    return render(request,'welcome.html',{'ImportantDate':Important_Date})
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
def EditProfile(request):

    if request.method == 'POST':

        usern = request.user.username        
        email = request.POST.get('id_email')
        auth = request.POST.get('D_Auth')
        chid = request.POST.get('D_ChID')
        utyp = request.POST.get('U_Type')
        loss = request.POST.get('N_Loss')

        if loss == 'on':
            flos = True
        else:
            flos = False

        if usern is None:
            messages.info(request, 'You must enter Username')
            return redirect('edit_profile')

        elif email is None:
            messages.info(request, 'You must enter Email')
            return redirect('edit_profile')

        elif User.objects.filter(username=usern).exists():
            messages.info(request, 'Username is already taken')
            return redirect('edit_profile')

        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already Taken')
            return redirect('edit_profile')

        elif auth is None:
            messages.info(request, 'Authentication Key Must be Entered')
            return redirect('edit_profile')

        elif chid is None:
            messages.info(request, 'Channel ID Must be Entered')
            return redirect('edit_profile')

        elif UserAuthentication.objects.filter(D_Auth=auth).exists():
            messages.info(request, 'Authentication key in Use')
            return redirect('edit_profile')

        else:
            user = User.objects.get(username=user)
            userauth_obj = UserAuthentication.objects.update(
                U_User = user,
                defaults = {
                    "D_Auth": auth,
                    "D_ChID": chid,
                    "U_Type": utyp,
                    "N_Loss": flos,
                }
            )
            user_obj = User.objects.update(
                defaults = {
                "username": username,
                "email": email
                }
            )

    return render(request, 'registration/edit_profile.html')

@login_required(login_url='login')
def Bid_Screen(request): 
    random_object =Bid_Bucket.objects.filter(Current_player = True)
    context = {
        "random_object": random_object
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