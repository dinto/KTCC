from django.shortcuts import render,HttpResponse,redirect 
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate,login,logout 
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreatePlayer
from KTCC.models import PlayerInfo

# Create your views here.

@login_required(login_url='login')
def KTCC(request): 
    return render(request,'index.html',{})

def welcome(request): 
    return render(request,'welcome.html',{})
    #return render(request,'Teams.html',{})

def Teams(request): 
    return render(request,'Teams.html',{})

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
            return redirect('login')
    return render (request,'Authentication/signup.html')

def LoginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('home')
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
            return redirect("home")
        #messages.success(request, "Player Registration Successfully!")
        
    else:
        forms = CreatePlayer()
    context = {
        "forms": forms
    }
    return render(request, "registration.html", context)
