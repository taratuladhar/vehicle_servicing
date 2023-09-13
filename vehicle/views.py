
from django.shortcuts import render,HttpResponse,redirect
from . import forms,models
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login,logout as auth_logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.hashers import make_password
# from django.urls import reverse
from django.shortcuts import get_object_or_404



# Create your views here.
def homePage(request):
    return render(request,'vehicle/index.html')

def loginPage(request):
    return render(request,"vehicle/login.html")

def registerPage(request):
    return render(request,"vehicle/register.html")

# def appointmentPage(request):
#     return render(request,"vehicle/appointment.html")


def register(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}
    
    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST)
        
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.password = make_password(userForm.cleaned_data['password'])
            user.save()
            
            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()
            
            # Get or create the customer group and add the user to it
            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)
            
            return HttpResponseRedirect('/login')
    
    return render(request, 'vehicle/register.html', context=mydict)


def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect('/')
        else:
            error_message = "Invalid login credentials. Please try again."
            return render(request, 'vehicle/login.html', {'error_message': error_message})
    return render(request, 'vehicle/login.html')
    
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def customer_add_appointment(request):
    # if request.method=='POST':
    #     form = forms.AppointmentForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('/')  # Create an 'appointment_success' URL
    # else:
    #     form = forms.AppointmentForm()

    # context = {'form': form}
    # return render(request, 'vehicle/customer_add_appointment.html', context)
    customer=models.Customer.objects.get(user_id=request.user.id)
    enquiry=forms.AppointmentForm()
    if request.method=='POST':
        enquiry=forms.AppointmentForm(request.POST)
        if enquiry.is_valid():
            # customer=models.Customer.objects.get(user_id=request.user.id)
            enquiry_x=enquiry.save(commit=False)
            enquiry_x.customer=customer
            enquiry_x.save()
            
            # selected_services = request.POST.getlist('servicing')
            # enquiry_x.servicing.set(selected_services)
            
            # enquiry_x.save()
            return redirect('customer_dashboard')
        else:
            print("form is invalid")
            print(enquiry.errors)
            
    return render(request,'vehicle/customer_add_appointment.html',{'enquiry':enquiry,'customer':customer})



@login_required
def customer_dashboard(request):
    enquiry=models.Appointment.objects.all().order_by('-id')
    customers=[]
    for enq in enquiry:
        customer=models.Customer.objects.get(id=enq.customer_id)
        customers.append(customer)
    return render(request, 'vehicle/customer_dashboard.html',{'data':zip(customers,enquiry)})
  
@login_required  
def customer_delete_appointment(request,pk):
    # customer=models.Customer.objects.get(user_id=request.user.id)
    
    # enquiry=models.Appointment.objects.get(id=pk)
    # enquiry.delete()
    # return redirect('customer_dashboard')    

     # Use get_object_or_404 to retrieve the appointment if it exists
    enquiry = get_object_or_404(models.Appointment, id=pk)

    # Check if the logged-in user is the owner of the appointment
    if enquiry.customer.user != request.user:
        # If not, return an error response or handle it as needed
        return HttpResponseForbidden("You do not have permission to delete this appointment.")

    # Delete the appointment
    enquiry.delete()

    # Redirect to the customer dashboard
    return redirect('customer_dashboard')

@login_required
def customer_profile(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    return render(request,'vehicle/customer_profile.html',{'customer':customer})

@login_required
def edit_customer_profile(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    user=models.User.objects.get(id=customer.user_id)
    print("1")
    userForm=forms.CustomerUserForm(instance=user)
    customerForm=forms.CustomerForm(instance=customer)
    print("2")

    mydict={'userForm':userForm,'customerForm':customerForm,'customer':customer}
    if request.method=='POST':
        print("3")

        userForm=forms.CustomerUserForm(request.POST,instance=user)
        print("4")
        customerForm=forms.CustomerForm(request.POST,instance=customer)
        print("5")
        if userForm.is_valid():
            print("6")
            user=userForm.save()
            print("7")
            print("8")
            user.save()
            print("9")
        if customerForm.is_valid():
            customerForm.save()
            print("10")
            
            return redirect('customer_profile')
    return render(request,'vehicle/edit_customer_profile.html',context=mydict)

@login_required
def customer_feedback(request):
    customer=models.Customer.objects.get(user_id=request.user.id)
    print("1")
    feedback=forms.FeedbackForm()
    print("2")
    if request.method=='POST':
        print("3")
        feedback=forms.FeedbackForm(request.POST)
        print("4")
        if feedback.is_valid():
            print("5")
            feedback.save()
            
        else:
            print("form is invalid")
            print(feedback.errors)
        return render(request,'vehicle/feedback_sent.html',{'customer':customer})
    return render(request,'vehicle/customer_feedback.html',{'feedback':feedback,'customer':customer})