"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from home import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('reg/', views.user_register, name='register'),
    path('vrfotp/',views.verify_otp,name='verifyotp'),
    path('passreset/',views.pass_reset_request,name='reqpsw'),
    path('otp_confirm/', views.otp_confirm, name='otp_confirm'),
    path('set_password/', views.password_reset, name='password_reset'),
    path('logout/', views.user_logout, name='logout'),

]
