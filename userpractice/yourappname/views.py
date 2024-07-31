from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django import forms
from twilio.rest import Client
from django.conf import settings
import random
from django.core.exceptions import ValidationError

def validate_phone_number(value):
    if not value.startswith('+63') or len(value) != 13:
        raise ValidationError('Invalid Philippine phone number format.')

class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    phone_number = forms.CharField(max_length=15, validators=[validate_phone_number])
    password = forms.CharField(widget=forms.PasswordInput)
    reenter_password = forms.CharField(widget=forms.PasswordInput)
    
class LoginForm(forms.Form):
    identifier = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

def send_otp(phone_number, otp):
    # Ensure the phone number is in E.164 format
    if phone_number.startswith('0'):
        formatted_phone_number = '+63' + phone_number[1:]
    else:
        formatted_phone_number = phone_number
    
    # Twilio credentials
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    twilio_phone_number = settings.TWILIO_PHONE_NUMBER
    
    client = Client(account_sid, auth_token)
    
    try:
        message = client.messages.create(
            body=f"Your OTP code is {otp}",
            from_=twilio_phone_number,
            to=formatted_phone_number
        )
        return True
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        return False

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            reenter_password = form.cleaned_data['reenter_password']
            
            if password == reenter_password:
                if not MyUser.objects.filter(username=username).exists():
                    if phone_number.startswith('+63') or phone_number.startswith('0'):
                        otp = random.randint(100000, 999999)
                        request.session['otp'] = otp
                        request.session['phone_number'] = phone_number
                        request.session['username'] = username
                        request.session['password'] = password
                        if send_otp(phone_number, otp):
                            return redirect('verify_otp')
                        else:
                            messages.error(request, 'Failed to send OTP')
                    else:
                        messages.error(request, 'Invalid phone number. Ensure it starts with +63 or 0.')
                else:
                    messages.error(request, 'Username already exists')
            else:
                messages.error(request, 'Passwords do not match')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        if otp == str(request.session.get('otp')):
            username = request.session.get('username')
            phone_number = request.session.get('phone_number')
            password = request.session.get('password')
            MyUser.objects.create_user(username=username, phone_number=phone_number, password=password)
            del request.session['otp']
            del request.session['phone_number']
            del request.session['username']
            del request.session['password']
            return redirect('login')
        else:
            messages.error(request, 'Invalid OTP')
    return render(request, 'verify_otp.html')

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']
            user = authenticate(request, username=identifier, phone_number=identifier, password=password)
            if user:
                auth_login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def home(request):
    return render(request, 'home.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
