from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

def signup(request):
    return render(request, 'signup.html')

def verify(request):
    return render(request, 'verify.html')

def tutorial(request):
    return render(request, 'tutorial.html')

def login(request):
    return render(request, 'login.html')

def survey(request):
    return render(request, 'survey.html')

def home(request):
    return render(request, 'home.html')

def homedish(request, dish_id):
    # Replace this with actual dish retrieval logic
    return render(request, 'homedish.html')

def saved(request):
    return render(request, 'saved.html')

def saveddish(request, dish_id):
    # Replace this with actual dish retrieval logic
    return render(request, 'saveddish.html')

def cooked(request):
    return render(request, 'cooked.html')

def about(request):
    return render(request, 'about.html')  # Make sure you have 'about.html' template

def faqs(request):
    return render(request, 'faqs.html')

def terms(request):
    return render(request, 'terms.html')

#@login_required
def settings(request):
    return render(request, 'settings.html')

#@login_required
def editprofile(request):
    
    return render(request, 'editprofile.html')

#@login_required
def mealpref(request):
    
    return render(request, 'mealpref.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
