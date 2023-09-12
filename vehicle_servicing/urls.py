from django.contrib import admin
from django.urls import path
from vehicle import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("",views.homePage, name='home'),
    path("login_page/",views.loginPage,name='login-page'),
    path("register_page/",views.registerPage,name='register-page'),
    
    # path('appointment/', views.appointment, name='appointment'),
    
    path("login/",views.login, name='login'),
    path("register/",views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    
    path("customer_dashboard/",views.customer_dashboard, name='customer_dashboard'),
    path('customer_add_appointment/', views.customer_add_appointment, name='customer_add_appointment'),
    path('customer_delete_appointment/<int:pk>', views.customer_delete_appointment,name='customer_delete_appointment'),
    path("customer_profile/",views.customer_profile, name='customer_profile'),
    path("edit_customer_profile/",views.edit_customer_profile, name='edit_customer_profile'),
    # path(" ",views.customer_dashboard, name='customer_dashboard'),
]