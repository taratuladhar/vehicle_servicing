from django.contrib import admin
from django.urls import path
from vehicle import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",views.homePage, name='home'),
    path("login_page/",views.loginPage,name='login-page'),
    path("register_page/",views.registerPage,name='register-page'),
    
    path('appointments/', views.appointmentPage, name='appointment'),
    
    path("login/",views.login, name='login'),
    path("register/",views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    # path("dashboard/",views.customer_dashboard, name='customer_dashboard'),
    # path(" ",views.customer_profile, name='customer_profile'),
    # path(" ",views.edit_customer_profile, name='edit_customer_profile'),
    # path(" ",views.customer_dashboard, name='customer_dashboard'),
]