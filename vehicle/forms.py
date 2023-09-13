from django import forms
from django.contrib.auth.models import User
from . import models

class CustomerUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=['username','email','password','confirm_password']
        widgets = {
        'password': forms.PasswordInput()
        }
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match")
        
        
class CustomerForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['contact','address','profile_pic']
        
class AppointmentForm(forms.ModelForm):
    class Meta:
        model=models.Appointment
        fields=['vehicle_number', 'vehicle_model', 'description', 'wheelers', 'servicing', 'submission_date']
           
class FeedbackForm(forms.ModelForm):
    class Meta:
        model=models.Feedback
        fields=['by','message']
        by = forms.CharField(required=True)
    message = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 3}))