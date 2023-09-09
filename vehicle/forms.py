from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['contact','address','profile_pic']
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model=models.Appointment
        fields=['vehicle_number', 'vehicle_model', 'description', 'wheelers', 'servicing', 'submission_date']
           