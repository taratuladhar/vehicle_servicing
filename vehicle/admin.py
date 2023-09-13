from django.contrib import admin
from .models import Customer, Appointment,Feedback

# Register your models here

admin.site.register(Customer)
admin.site.register(Appointment)
admin.site.register(Feedback)