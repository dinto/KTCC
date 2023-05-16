from django.db import models

# Create your models here.
class PlayerInfo(models.Model):
    
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
        unique_together = ["mail_id"]
        verbose_name_plural = 'Player List'

    def __str__(self):
        return self.name
