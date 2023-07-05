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
from KTCC.models import VideoLink,CurrentBid,Season,ImportantDate,Available_Point_Table,Bid_Details,Unsold_player,Schedule,TeamInfo,Bid_Bucket,PlayerInfo,AUCTIONRULE
from reportlab.platypus import Image
from django.db.models import Q
from django.template import loader 
from .utils import mobileBrowser
from django.templatetags.static import static
import csv
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

@login_required(login_url='login')
def KTCC(request): 
    Important_Date = ImportantDate.objects.all()
    Videos_models= VideoLink.objects.all().order_by('-id')
    p = Paginator(Videos_models,3)
    page = request.GET.get('page')
    Videos = p.get_page(page)
    nums = "a" * Videos.paginator.num_pages
    if mobileBrowser (request):
        return render(request,'m_index.html',{'ImportantDate':Important_Date,'Videos':Videos,'nums':nums})
    else:
        return render(request,'index.html',{'ImportantDate':Important_Date,'Videos':Videos,'nums':nums})

def welcome(request): 
    Important_Date = ImportantDate.objects.all()
    Videos_models= VideoLink.objects.all().order_by('-id')
    p = Paginator(Videos_models,3)
    page = request.GET.get('page')
    Videos = p.get_page(page)
    nums = "a" * Videos.paginator.num_pages
    Auction_rules=AUCTIONRULE.objects.all().order_by('id')
    return render(request,'welcome.html',{'ImportantDate':Important_Date,'Videos':Videos,'nums':nums,'Auction_rules':Auction_rules})
    #return render(request,'Teams.html',{})

def Teams(request): 
    Teams= TeamInfo.objects.all()
    posts = list(TeamInfo.objects.all())
    posts = [posts[i:i+2] for i in range(0, len(posts), 2)]
    Remaining_Point=Available_Point_Table.objects.all()
    if mobileBrowser (request):
        return render(request,'m_Teams.html',{'Teams':Teams,'Remaining_Point':Remaining_Point,'posts':posts})
    else:
        return render(request,'Teams.html',{'Teams':Teams,'Remaining_Point':Remaining_Point,'posts':posts})

def Players(request): 
   # players= PlayerInfo.objects.all()
    Players_model= PlayerInfo.objects.all().order_by('-id')
    p = Paginator(Players_model,3)
    page = request.GET.get('page')
    players_paginaton = p.get_page(page)
    nums = "a" * players_paginaton.paginator.num_pages

    if request.method == "GET" and 'search' in request.GET: 
        query =request.GET.get('query')
        if query:
            #search=PlayerInfo.objects.filter(name__icontains=query)
            search=PlayerInfo.objects.filter(Q(name__icontains=query) | Q(Role__icontains=query) | Q(Batting_style__icontains=query) | Q(Bowling_style__icontains=query))
          #  return render(request,'Players.html',{'players':search})   
            if mobileBrowser (request):
                return render(request,'m_Players.html',{'players_paginaton':search,'nums':nums}) 
            else:
                return render(request,'Players.html',{'players_paginaton':search,'nums':nums}) 

            #return render(request,'Players.html',{'players_paginaton':search,'nums':nums}) 
   # return render(request,'Players.html',{'players':players,'players_paginaton':players_paginaton,'nums':nums})
    if mobileBrowser (request):
        return render(request,'m_Players.html',{'players_paginaton':players_paginaton,'nums':nums})
    else:
        return render(request,'Players.html',{'players_paginaton':players_paginaton,'nums':nums})
    

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

    #return render (request,'Authentication/login.html')
    if mobileBrowser (request):
        return render (request,'Authentication/m_login.html')
    else:
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
    season=Season.objects.all()
    is_player_Registation_closed=season[0].is_player_Registation_closed
    context = {
        "forms": forms,
        "is_player_Registation_closed":is_player_Registation_closed,

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
    season=Season.objects.all()
    is_team_creation_closed=season[0].is_team_creation_closed
    context = {
        "forms": forms,
        "is_team_creation_closed":is_team_creation_closed,
    }
    return render(request, "profile.html", context)

@login_required(login_url='login')
def Bid_Screen(request): 
    if request.user.is_authenticated:
        username = request.user.username
        logged_team =TeamInfo.objects.filter(Users =  request.user.id)
        if request.user.is_superuser:
            Remaining_Point= 0
        else:
            Remaining_Point=Available_Point_Table.objects.filter(Team_Name=logged_team[0])[0]
    random_object =Bid_Bucket.objects.filter(Current_player = True)
    CurrentBids = CurrentBid.objects.all()
    Base_piont=Season.objects.values('Base_Point_For_Player')[0]['Base_Point_For_Player']
    Team=TeamInfo.objects.filter(Users = request.user)
    Players_count=Bid_Details.objects.filter(Team_Name=Team[0].id).count()
    Minimum_Players_Per_Team=Season.objects.values('Minimum_Players_Per_Team')[0]['Minimum_Players_Per_Team']
    reservePlayers=Minimum_Players_Per_Team-Players_count
    if(reservePlayers>0):
        reserve_point=(reservePlayers-1)*Base_piont
    else:
        reserve_point=0
    current_team =TeamInfo.objects.filter(Users = request.user.id)
    Available_Point=Available_Point_Table.objects.filter(Team_Name=current_team[0])
    Max_Available_point_To_bid=int(Available_Point[0].Available_Point)-int(reserve_point)
    if request.method == "POST" and 'Increment' in request.POST: 
        current_user = request.user
        Bid_Bucket_current_player_count=Bid_Bucket.objects.filter(Current_player = True).count()
        if(Bid_Bucket_current_player_count):
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
                #if(Available_Point[0].Available_Point>=incremental):
                if(Max_Available_point_To_bid>=incremental):    
                
                    CurrentBid_details.update(Team_Name=current_team[0],Current_Bid_Point=incremental)
            else:
                current_team =TeamInfo.objects.filter(Users = current_user.id)
                Available_Point=Available_Point_Table.objects.filter(Team_Name=current_team[0])
                #if(Available_Point[0].Available_Point>=1000):
                if(Max_Available_point_To_bid>=1000):
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
            "Base_piont":Base_piont,
            "Remaining_Point":Remaining_Point,
            "Players_count":Players_count,
            "reserve_point":reserve_point,
            "Max_Available_point_To_bid":Max_Available_point_To_bid,
        }
        if mobileBrowser (request):
            return render(request, "mobile_Bid_screen.html",context)
        else:
            return render(request, "Bid_Screen.html",context)
        
    context = {
        "random_object": random_object,
        "CurrentBid":CurrentBids,
        "username":username,
        "Base_piont":Base_piont,
        "Remaining_Point":Remaining_Point,
        "Players_count":Players_count,
        "reserve_point":reserve_point,
        "Max_Available_point_To_bid":Max_Available_point_To_bid,
    }
    if mobileBrowser (request):
        return render(request, "mobile_Bid_screen.html",context)
    else:
        return render(request, "Bid_Screen.html",context)


@login_required(login_url='login')
def Bid_Screen_new_Player(request): 
    Bid_bucket_count=Bid_Bucket.objects.count()
    if request.method == "POST" and 'StartBid' in request.POST: 
        Bid_bucket_count=Bid_Bucket.objects.count()
        #new code added for after bid compele again start bid click means it never load to bidbucket
        Bid_already_Started=Bid_Details.objects.all()
        is_bid_started=0
        for check in Bid_already_Started:
            if(check.Player_name.is_icon_player==False):
                is_bid_started +=1          
            else:
                pass
        if(Bid_bucket_count<1 and is_bid_started==0):
        #new code end    
            players= PlayerInfo.objects.filter(is_icon_player=False).all()
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
            if(Bid_Bucket.objects.filter(Current_player = True).count()):
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

    if(Bid_bucket_count>0):
        Unsold_player_count=Unsold_player.objects.count()
        Sold_player_count=Bid_Details.objects.count()
        current_bid_player_count =Bid_Bucket.objects.filter(Current_player = True).count()
        Base_piont=Season.objects.values('Base_Point_For_Player')[0]['Base_Point_For_Player']
        CurrentBids = CurrentBid.objects.all()
        if(current_bid_player_count>0):
            random_object =Bid_Bucket.objects.filter(Current_player = True)
            context = {
                "random_object": random_object,
                "CurrentBid":CurrentBids,
                "Base_piont":Base_piont,
                "Bid_bucket_count":Bid_bucket_count,
                "Unsold_player_count":Unsold_player_count,
                "Sold_player_count":Sold_player_count
            }
            if mobileBrowser (request):
                return render(request, "m_Bid_screen_new_player.html",context)
            else:
                return render(request, "Bid_screen_new_player.html",context)
        else:
            if request.method == "POST" and 'NewPlayer' in request.POST: 
                random_object_db = Bid_Bucket.objects.all()[randint(0, Bid_bucket_count - 1)] #single random object
                Bid_Bucket.objects.filter(Player_name = random_object_db.Player_name).update(Current_player = True)
                random_object =Bid_Bucket.objects.filter(Current_player = True)
                context = {
                "random_object": random_object,
                "CurrentBid":CurrentBids,
                "Base_piont":Base_piont,
                "Bid_bucket_count":Bid_bucket_count,
                "Unsold_player_count":Unsold_player_count,
                "Sold_player_count":Sold_player_count
                }
                if mobileBrowser (request):
                    return render(request, "m_Bid_screen_new_player.html",context)
                else:
                    return render(request, "Bid_screen_new_player.html",context)
    Unsold_player_count=Unsold_player.objects.count()
    Sold_player_count=Bid_Details.objects.count()
    context = {
    "Bid_bucket_count":Bid_bucket_count,
    "Unsold_player_count":Unsold_player_count,
    "Sold_player_count":Sold_player_count
    }
    if mobileBrowser (request):
        return render(request, "m_Bid_screen_new_player.html",context)
    else:
        return render(request, "Bid_screen_new_player.html",context)


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
    Unsold_players = Unsold_player.objects.all()
    posts_Bid_Details = list(Bid_Details.objects.all().order_by('-id'))
    column_num=3
    posts_Bid_Details = [posts_Bid_Details[i:i+column_num] for i in range(0, len(posts_Bid_Details), column_num)]
    #Players_model= PlayerInfo.objects.all().order_by('-id')
    p = Paginator(posts_Bid_Details,column_num*1)
    page = request.GET.get('page')
    sold_players_paginaton = p.get_page(page)
    nums = "a" * sold_players_paginaton.paginator.num_pages


    if request.method == "GET" and 'search' in request.GET: 
        query =request.GET.get('query')
        if query:
            search=Bid_Details.objects.filter(Player_name__name__icontains=query)
            context = {
                "Sold_Players":search,
                "posts_Bid_Details":posts_Bid_Details,
                "sold_players_paginaton":sold_players_paginaton,
                "nums":nums
            }
            return render(request, "BidStatusnew.html",context)
    if request.method == "GET" and 'search_unsold' in request.GET: 
        query =request.GET.get('query_unsold')
        if query:
            search=Unsold_player.objects.filter(Player_name__name__icontains=query)
            context = {
                "UnSold_Players":search
            }
            return render(request, "BidStatusnew.html",context)

    context = {
        "Sold_Players":Sold_Players,
        "Unsold_players":Unsold_players,
        "posts_Bid_Details":posts_Bid_Details,
        "sold_players_paginaton":sold_players_paginaton,
        "nums":nums

    }
    return render(request, "BidStatusnew.html",context)

def Team_players(request,id):
    Team_name=TeamInfo.objects.get(id=id)
    #print(Bid_Details.objects.filter(Team_Name=Team_name.id))
    Team_players = Bid_Details.objects.filter(Team_Name=Team_name.id)
    #Team_players = list(Bid_Details.objects.filter(Team_Name=Team_name.id))
    #Team_players = [Team_players[i:i+2] for i in range(0, len(Team_players), 2)]
    context = {
        "Team_players":Team_players,
        "Team_name":Team_name
    }
    return render(request, "Team_Players.html",context)


def Myauction(request,id):
    Team_name=TeamInfo.objects.get(id=id)
    Team_players = Bid_Details.objects.filter(Team_Name=Team_name.id)
    context = {
        "Team_players":Team_players,
        "Team_name":Team_name
    }
    return render(request, "Team_Players.html",context)

def Icon_Player(request):
    #Players = Bid_Details.objects.get()
    #context = {
    #    "Sold_Players":Sold_Players
    #}
    return render(request, "Icon_Player_selection.html")


def GenerateRegisteredPlayersInfo(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer,pagesize=letter,bottomup=0)
    textob=p.beginText()
    textob.setTextOrigin(inch,inch)
    textob.setFont("Helvetica",14)
    players= PlayerInfo.objects.all()
    lines =[]
    for player in players:   
        lines.append(player.Season)
        imagepath='/static/'+ str(player.Profile_Pic)
        #url = static(str(player.Profile_Pic))
        #print(url)
        #p.drawImage(url,-0.8*inch,9.3*inch)
       # p.drawInlineImage('https://www.plus2net.com/images/top2.jpg',2.2*inch,2.2*inch )
       # lines.append(Image('static/images/LogoT10.jpeg',2.2*inch,2.2*inch))
        lines.append(player.Profile_Pic)
        lines.append(player.name)
        lines.append(player.Role)
        lines.append(player.phone_number)
    for line in lines:
        textob.textLine(str(line))
    p.drawText(textob)
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='RegisteredPlayers.pdf')

def players_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] ='attcahment;filename=playersregistration.csv'
    writer =csv.writer(response)
    players= PlayerInfo.objects.all().order_by('id')
    writer.writerow(['Registration No','Name','Date of Birth','Age','Place','Phone Number','Mail Id','Role','Batting Style','Bowling Style','is home ground player','is icon player'])

    for player in players:
        if(player.is_home_ground_player):
            home_ground_player="YES"
        else:
            home_ground_player="NO"
        if(player.is_icon_player):
            icon_player="YES"
        else:
            icon_player="NO"
        writer.writerow([player.id,player.name,player.dob,player.age,player.place,player.phone_number,player.mail_id,player.Role,player.Batting_style,player.Bowling_style,home_ground_player,icon_player])

    return response

def Sold_players_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] ='attcahment;filename=SoldPlayers.csv'
    writer =csv.writer(response)
    players= Bid_Details.objects.all().order_by('id') 
    writer.writerow(['Registration No','Player Name','Sold Point ','Team Name','Season'])

    for player in players:
        regi=PlayerInfo.objects.all().filter(name=player.Player_name.name)
        writer.writerow([regi[0].id,player.Player_name.name,player.Sold_Point,player.Team_Name,player.Season])

    return response

def Unsold_players_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition'] ='attcahment;filename=UnSoldPlayers.csv'
    writer =csv.writer(response)
    players= Unsold_player.objects.all().order_by('id')
    writer.writerow(['Registration No','Player Name','Season'])

    for player in players:
        regi=PlayerInfo.objects.all().filter(name=player.Player_name.name)
        writer.writerow([regi[0].id,player.Player_name.name,player.Season])

    return response
    
def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def GeneratePdf(request):
    players= PlayerInfo.objects.all().order_by('id')
    #players= PlayerInfo.objects.filter(name='DINTO DAVI T')
    data = {
    "players": players,
    }
    pdf = render_to_pdf('Registedplayerspdf.html',data)
    if pdf:
        response=HttpResponse(pdf,content_type='application/pdf')
        filename = "PLAYERSLIST.pdf"
        content = "inline; filename= %s" %(filename)
        response['Content-Disposition']=content
        return response
    return HttpResponse("Page Not Found")