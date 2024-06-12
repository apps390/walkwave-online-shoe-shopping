from django.http import HttpResponse
from django.shortcuts import render, redirect
from shop.models import Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.
def generate_otp():
    return random.randint(1000, 9999)


def send_otpemail(email, otp, user):
    subject = 'Verify Your One-Time-Password'
    message = (f'Dear {user},\n\n'
               f'Greetings from Belstaff Team  ,Your OTP for verification is {otp}')
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(subject, message, email_from, email_to)


def home(request):
    c = Category.objects.all()
    return render(request, 'index.html', {'c': c})


def user_login(request):
    if request.method == "POST":
        u = request.POST['user']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return home(request)
        else:
            messages.error(request, 'invalid username/password')
            print(messages)
            return redirect('home:login')
    return render(request, 'login.html')


def user_register(request):
    if (request.method == 'POST'):
        u = request.POST['username']
        p = request.POST['password']
        eml = request.POST['email']
        fnm = request.POST['fname']
        lnm = request.POST['lname']
        try:
            if User.objects.filter(username=u).exists():
                messages.warning(request, 'username already taken')
                return redirect('home:register')
        except:
            pass
        if len(p) < 8:
            messages.warning(request, 'password must be 8 character')
            return redirect('home:register')
        if '@' not in eml:
            messages.warning(request, 'invalid email !')
            return redirect('home:register')
        otp = generate_otp()
        request.session['temp_user_data'] = {
            'username': u,
            'password': p,
            'email': eml,
            'fnm': fnm,
            'lnm': lnm,
            'otp': otp
        }
        send_otpemail(eml, otp, u)
        messages.success(request, 'An OTP has been sent to your email-id')
        return redirect('home:verifyotp')
    return render(request, 'register.html')

def verify_otp(request):
    if request.method == 'POST':
        input_otp = request.POST['otp']
        temp_user_data = request.session.get('temp_user_data')
        if temp_user_data is not None:
            if input_otp == str(temp_user_data['otp']):
                user = User.objects.create_user(
                    username=temp_user_data['username'],
                    password=temp_user_data['password'],
                    email=temp_user_data['email'],
                    first_name=temp_user_data['fnm'],
                    last_name=temp_user_data['lnm'],

                )
                user.save()
                del request.session['temp_user_data']
                return redirect('home:login')
            else:
                messages.error(request, 'invalid OTP!')
        else:
            messages.warning(request, 'invalid session!')
            return redirect('home:register')
    return render(request, 'verifyotp.html')


def resetpassword_otp(email, otp, user):
    subject = 'Reset password'
    message = (f'Dear {user},\n\n'
               f'OTP for your password reset is {otp}'
               f'\n\n With regards\n Belstaff team')
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(subject, message, email_from, email_to)


def pass_reset_request(request):
    if request.method == 'POST':
        u = request.POST['user_data']
        user_data = User.objects.filter(username=u).exists()
        if user_data is not None:
            user_details=User.objects.get(username=u)
            print(user_details.email)
            user = user_details.username
            user_email = user_details.email
            get_otp = generate_otp()
            request.session['temp_user_data'] = {
                'username': user,
                'email': user_email,
                'otp': get_otp
            }
            resetpassword_otp(user_email, get_otp, u)
            messages.success(request, 'An OTP has been sent to your email-id for password-reset')
            return redirect('home:otp_confirm')
        else:
            messages.error(request, 'Invalid Username')
    return render(request, 'pasword_reset.html')



def otp_confirm(request):
    if request.method == 'POST':
        input_otp = request.POST['otp']
        temp_user_data = request.session.get('temp_user_data')
        if input_otp == str(temp_user_data['otp']):
            return redirect('home:password_reset')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'password_otp.html')



def password_reset(request):
    if request.method == 'POST':
        password = request.POST['password1']
        cnf_password = request.POST['password2']
        if password == cnf_password:
            temp_user_data = request.session.get('temp_user_data')
            if temp_user_data:
                user = User.objects.get(username=temp_user_data['username'])
                if user is not None:
                    user.set_password(password)
                    user.save()
                    del request.session['temp_user_data']
                    messages.success(request, ' Your password has been changed successfully!')
                    return redirect('home:login')

                else:
                    messages.error(request, 'Username is Incorrect')
            else:
                messages.error(request, 'Session Expired')
        else:
            messages.error(request, ' Password Mismatch')
    return render(request, 'password_rest_confirm.html')


def user_logout(request):
    logout(request)
    return home(request)
