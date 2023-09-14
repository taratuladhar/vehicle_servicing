from django.db import models
from django.contrib.auth.models import User
# from django.core.mail import send_mail
# from django.db.models.signals import post_save
# from django.dispatch import receiver

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
    # status = models.CharField(max_length=20, choices=[("Approved", "Approved"), ("Processing", "Processing"), ("Completed", "Completed")])
    customer=models.ForeignKey('Customer', on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_model}"
    
class Feedback(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=40)
    message=models.CharField(max_length=500)
    
    def __str__(self):
        return self.by
    
# @receiver(post_save, sender=Appointment)
# def send_status_email(sender, instance, **kwargs):
#     # Define the subject and message for the email
#     subject = 'Appointment Status Update'
#     message = f'Your appointment with ID {instance.id} has been {instance.status}.'

#     # Specify the sender and recipient email addresses
#     from_email = 'your_email@gmail.com'  # Replace with your email address
#     recipient_email = instance.customer.user.email

#     # Send the email
#     send_mail(subject, message, from_email, [recipient_email])