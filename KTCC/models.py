from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Season(models.Model):
    Season_Name=models.CharField(max_length=100)
    Maximum_Bid_Point= models.IntegerField()
    Maximum_Players_Per_Team =models.IntegerField()
    Minimum_Players_Per_Team =models.IntegerField()
    Winning_point=models.IntegerField()
    NR_point=models.IntegerField()
    Total_over_Per_Innings=models.IntegerField()
    
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

    class Meta:
        unique_together = ["mail_id","Season"]
        verbose_name_plural = 'Player List'

    def __str__(self):
        return self.name


class TeamInfo(models.Model):
    Team_Name = models.CharField(max_length=100)
    Short_Name = models.CharField(max_length=100)
    Team_Logo = models.ImageField(null=True,blank=True, upload_to='Team_Logo/')
    Season = models.ForeignKey(Season,on_delete=models.CASCADE)
    Users = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Team_Name","Season"]
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
        return self.Player_name

class Bid_Details(models.Model):
    Player_name = models.ForeignKey(PlayerInfo,  on_delete=models.CASCADE)
    Status = models.CharField(max_length=100) #sold or unsold
    Sold_Point = models.IntegerField(blank=True, null=True)
    Team_Name = models.ForeignKey(TeamInfo,on_delete=models.CASCADE)
    Season = models.ForeignKey(Season,  on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Player_name","Season"]

    def __str__(self):
        return self.Player_name

class Available_Point_Table(models.Model):
    Team_Name = models.ForeignKey(TeamInfo, on_delete=models.CASCADE)
    Available_Point = models.IntegerField()
    Season = models.ForeignKey(Season,on_delete=models.CASCADE)

    class Meta:
        unique_together = ["Team_Name","Season"]

    def __str__(self):
        return self.Team_Name