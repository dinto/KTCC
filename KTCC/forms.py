from django import forms
from .models import PlayerInfo


class CreatePlayer(forms.Form):
    name = forms.CharField(label="Enter name",max_length=50) 
   # age = forms.NumberInput(label="age",max_length=50) 
   # dob = forms.DateInput(label="Enter DOB",max_length=50) 
   #             name = forms.CharField(label="Enter name",max_length=50) 
   #                 name = forms.CharField(label="Enter name",max_length=50) 
   #                     name = forms.CharField(label="Enter name",max_length=50) 
   #                         name = forms.CharField(label="Enter name",max_length=50) 
   #                             name = forms.CharField(label="Enter name",max_length=50) 
   #                                 name = forms.CharField(label="Enter name",max_length=50) 
   #                                     name = forms.CharField(label="Enter name",max_length=50) 
   #                                         name = forms.CharField(label="Enter name",max_length=50) 

  #  name = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dinto'})
    age = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 32'})
    dob = forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1990-08-04' ,'type': 'date'})
    gender= forms.Select(attrs={'class': 'form-control'})
    Pic_img = forms.FileField()
    country = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: INDIA'})
    state = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Kerala'})
    phone_number = forms.NumberInput(attrs={'class': 'form-control'})
    mail_id = forms.TextInput(attrs={'class': 'form-control'})
    aadharcard_no = forms.TextInput(attrs={'class': 'form-control'})
    aadharcard_img = forms.FileField()
    Role =  forms.Select(attrs={'class': 'form-control'})
    Batting_style = forms.Select(attrs={'class': 'form-control'})
    Bowling_style = forms.Select(attrs={'class': 'form-control'})
 #firstname = forms.CharField(label="Enter first name",max_length=50)  
  


   # class Meta:
   #     model = PlayerInfo
   #     exclude = ("Pic_img", "aadharcard_img",)
   #     'Pic_img': forms.FileField()

   #     widgets = {
   #         'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Dinto'}),
   #         'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 32'}),
   #         'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 1990-08-04' ,'type': 'date'}),
   #         'gender': forms.Select(attrs={'class': 'form-control'}),
            #'Pic_img': forms.FileField(),
   #         'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: INDIA'}),
   #         'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Kerala'}),
   #         'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
   #         'mail_id': forms.TextInput(attrs={'class': 'form-control'}),
   #         'aadharcard_no': forms.TextInput(attrs={'class': 'form-control'}),
   #         'aadharcard_img': forms.FileField(),
   #         'Role': forms.Select(attrs={'class': 'form-control'}),
   #         'Batting_style': forms.Select(attrs={'class': 'form-control'}),
   #         'Bowling_style': forms.Select(attrs={'class': 'form-control'}),

   #     }


        
        
       
     