from django import forms
from .models import PlayerInfo


class CreatePlayer(forms.ModelForm): 


    class Meta:
        model = PlayerInfo
        fields = '__all__'
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


        
        
       
     