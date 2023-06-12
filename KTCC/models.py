from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Season(models.Model):
    Season_Name=models.CharField(max_length=100)
    Maximum_Bid_Point= models.IntegerField()
    Base_Point_For_Player= models.IntegerField()
    ICON_Player_Point= models.IntegerField()
    Maximum_Players_Per_Team =models.IntegerField()
    Minimum_Players_Per_Team =models.IntegerField()
    youtube_Link = models.CharField(null=True,blank=True,max_length=100)
    facebook_Link= models.CharField(null=True,blank=True,max_length=100)
    instagram_Link = models.CharField(null=True,blank=True,max_length=100)
    phone_number=models.IntegerField() 
    mail_id=models.EmailField(max_length=100)
    Winning_point=models.IntegerField()
    NR_point=models.IntegerField()
    Total_over_Per_Innings=models.IntegerField()
    is_player_Registation_closed=models.BooleanField(default=False)
    is_team_creation_closed=models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'Season'
    def __str__(self):
        return self.Season_Name


class PlayerInfo(models.Model):

    Season = models.ForeignKey(Season,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    age = models.IntegerField()
    place = models.CharField(max_length=100)
    phone_number=models.IntegerField()
    mail_id= models.EmailField(max_length=100)
    gender_choice = (
        ("male", "Male"),
        ("Female", "Female"),
    )
    gender = models.CharField(choices=gender_choice, max_length=10)
    #country = models.CharField(max_length=100)
    #state = models.CharField(max_length=100)

    Role_choice = (
        ("Batsman", "Batsman"),
        ("Bowling Allrounder", "Bowling Allrounder"),
        ("Batting Allrounder", "Batting Allrounder"),
        ("Wicket-Keeper", "Wicket-Keeper"),
        ("Bowler", "Bowler"),
    )
    Role = models.CharField(choices=Role_choice, max_length=22)
    Hand_choice = (
        ("Right Handed Bat", "Right Handed Bat"),
        ("Left Handed Bat", "Left Handed Bat"),
    )
    Batting_style = models.CharField(choices=Hand_choice, max_length=22)

    Arm_choice = (
        ("Right-arm Fast Medium", "Right-arm Fast Medium"),
        ("Left-arm Fast Medium", "Left-arm Fast Medium"),
        ("Right-arm  Medium", "Right-arm  Medium"),
        ("Left-arm  Medium", "Left-arm  Medium"),
        ("right-arm legbreak", "right-arm legbreak"),
        ("right-arm offbreak", "right-arm offbreak"),
        ("Left-arm orthodox", "Left-arm orthodox"),
        ("Left-arm chinaman", "Left-arm chinaman"),
    )
    Bowling_style = models.CharField(choices=Arm_choice, max_length=22)
    
    aadharcard_no=models.CharField(max_length=100)
    #aadharcard_img = models.ImageField(null=True,blank=True, upload_to='aadharcard/')
    aadharcard = models.FileField(upload_to='aadharcard/')
    Profile_Pic = models.ImageField(null=True,blank=True, upload_to='Profile_Pic/')
    is_home_ground_player=models.BooleanField(default=False)
    is_icon_player=models.BooleanField(default=False)

    class Meta:
        unique_together = ["mail_id","Season"]
        verbose_name_plural = 'Player List'

    def __str__(self):
        return self.name + '   ' +self.mail_id 


class TeamInfo(models.Model):
    Team_Name = models.CharField(max_length=100)
    Short_Name = models.CharField(max_length=100)
    Manager_Name = models.CharField(max_length=100)
    Manager_Phone_Number=models.IntegerField()
    Owner_Name = models.CharField(max_length=100)
    Owner_Phone_Number=models.IntegerField()
    Team_Logo = models.ImageField(null=True,blank=True, upload_to='Team_Logo/')
    Season = models.ForeignKey(Season,on_delete=models.CASCADE)
    Users = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Users","Season"]
        verbose_name_plural = 'Team List'

    def __str__(self):
        return self.Team_Name

class CurrentBid(models.Model):
    Player_name = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    Current_Bid_Point = models.IntegerField()
    Team_Name = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    Season = models.ForeignKey(Season,on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Player_name","Season"]

    def __str__(self):
        return str(self.Player_name)

class Bid_Details(models.Model):
    Player_name = models.ForeignKey(PlayerInfo,  on_delete=models.CASCADE)
    Status = models.CharField(max_length=100) #open or sold or unsold
    Sold_Point = models.IntegerField(blank=True, null=True)
    Team_Name = models.ForeignKey(TeamInfo,on_delete=models.CASCADE)
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)
    #Current_player=models.BooleanField(default=False)

    class Meta:
        unique_together = ["Player_name","Season"]
        verbose_name_plural = 'Bid Details'

    def __str__(self):
        if self.Player_name==None:
            return "ERROR-Player_name IS NULL"
        return str(self.Player_name)
class Unsold_player(models.Model):
    Player_name = models.ForeignKey(PlayerInfo,  on_delete=models.CASCADE)
    Status = models.CharField(max_length=100) #open or sold or unsold
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Player_name","Season"]


class Available_Point_Table(models.Model):
    Team_Name = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    Available_Point = models.IntegerField()
    Season = models.ForeignKey(Season,on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Team_Name","Season"]

    def __str__(self):
        return str(self.Team_Name)

class Bid_Bucket(models.Model):
    Player_name = models.ForeignKey(PlayerInfo,  on_delete=models.CASCADE)
    Status = models.CharField(max_length=100) #open or sold or unsold
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)
    Current_player=models.BooleanField(default=False)

    class Meta:

        verbose_name_plural = 'Bid Bucket'

    def __str__(self):
        return str(self.Player_name)

class AUCTIONRULE(models.Model):
    Rules=models.CharField(max_length=700)
    class Meta:
        verbose_name_plural = 'AUCTION RULES'
    def __str__(self):
        return self.Rules

class VideoLink(models.Model):
    Youtube_Link=models.CharField(max_length=700)
    Title_Name=models.CharField(max_length=200)
    
    def __str__(self):
        return self.Title_Name

class ImportantDate(models.Model):
    EVENT=models.CharField(max_length=700)
    Start_Date = models.DateField()
    Start_Time=models.CharField(null=True,blank=True,max_length=100)
    End_Date = models.DateField()
    End_Time=models.CharField(null=True,blank=True,max_length=100)
    
    def __str__(self):
        return self.EVENT
    #class Meta:
    #    ordering = ['-Start_Date']

class Schedule(models.Model):
    Team1_Name= models.ForeignKey(TeamInfo, on_delete=models.CASCADE , related_name='Team1_Name')
    Team2_Name= models.ForeignKey(TeamInfo, on_delete=models.CASCADE , related_name='Team2_Name')
    Match_Number  = models.IntegerField()
    Date = models.DateField(null=True,blank=True)
    Time =models.CharField(null=True,blank=True,max_length=200) 
    Venue =models.CharField(null=True,blank=True,max_length=200) 
    Result =models.CharField(null=True,blank=True,max_length=200) 
    
    def __str__(self):
        return  str(self.Match_Number)  

class Pool_Master(models.Model):
    Pool_Name=models.CharField(max_length= 100)
    Team_Name = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ["Team_Name","Season"]

    def __str__(self):
        return self.Pool_Name


class PointTable(models.Model):
    Pool= models.ForeignKey(Pool_Master, on_delete=models.CASCADE)
    Team_Name = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    Match=models.IntegerField()
    Win_count= models.IntegerField()
    Lose_count= models.IntegerField()
    NR_count= models.IntegerField()
    Points= models.IntegerField()
    NRR=models.CharField(null=True,blank=True,max_length=200) 
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Team_Name","Season","Pool"]
        verbose_name_plural = 'Point Table'

    def __str__(self):
        return self.Team_Name

class Result(models.Model):
    Match_Number= models.ForeignKey(Schedule,  on_delete=models.CASCADE)
    Winning_Team= models.ForeignKey(TeamInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.Match_Number + self.Winning_Team
