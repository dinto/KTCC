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
        forms = CreatePlayer(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
            return redirect("Players")
    
    else:
        forms = CreatePlayer()
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