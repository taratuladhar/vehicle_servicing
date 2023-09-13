from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    contact=models.CharField(max_length=20, null=False)
    address=models.CharField(max_length=40)
    profile_pic=models.ImageField(upload_to='profile_pic/CustomerProfilePic/',null=True,blank=True)
    @property
    def get_name(self):
        return self.user.username
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.username
    
class Appointment(models.Model):
    VEHICLE_SERVICES = [
        (1, 'Washing'),
        (2, 'Waterless cleaning'),
        (3, 'Engine oil'),
        (4, 'Leakage'),
        (5, 'Maintenance'),
        (6, 'Full Servicing'),
    ]

    WHEELER_CHOICES= [
        ('two', 'Two Wheeler'),
        ('four', 'Four-Wheeler'),
    ]

    vehicle_number = models.CharField(max_length=20)  # Car number field
    vehicle_model = models.CharField(max_length=50)   # Car model field
    description = models.TextField(blank=True)
    wheelers = models.CharField(max_length=10, choices=WHEELER_CHOICES)
    servicing = models.ManyToManyField('self', choices=VEHICLE_SERVICES, blank=True, symmetrical=False)
    submission_date = models.DateTimeField()
    status=models.CharField(default="Pending", max_length=20)
    customer=models.ForeignKey('customer', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_model}"
    
class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)
    
    def __str__(self):
        return self.by