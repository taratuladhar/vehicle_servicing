
from django.shortcuts import render,HttpResponse,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required,user_passes_test

# Create your views here.
def homePage(request):
    return render(request,'vehicle/index.html')

def loginPage(request):
    return render(request,"vehicle/login.html")

def registerPage(request):
    return render(request,"vehicle/register.html")

def register(request):
    userForm=forms.CustomerUserForm()
    customerForm=forms.CustomerForm()
    mydict={'userForm':userForm,'customerForm':customerForm}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST)
        customerForm=forms.CustomerForm(request.POST)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customer=customerForm.save(commit=False)
            customer.user=user
            customer.save()
            my_customer_group = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group[0].user_set.add(user)
        return HttpResponseRedirect('login-page')
    return render(request,'vehicle/register.html',context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('customer_dashboard')
        else:
            # Handle invalid login credentials, display an error message, etc.
            return redirect('login-page')
    return render(request, 'vehicle/login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def customer_dashboard(request):
     customer=models.Customer.objects.get(user_id=request.user.id)
     return render(request,'vehicle/customer_dashboard.html',{'customer':customer})

@login_required
def customer_profile(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})

def edit_customer_profile(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(request.FILES,instance=customer)
    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        userForm=forms.CustomerUserForm(request.POST,instance=user)
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        if userForm.is_valid() and customerForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('customer_profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)