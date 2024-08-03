from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify/', views.verify, name='verify'),
    path('tutorial/', views.tutorial, name='tutorial'),
    path('login/', views.login, name='login'),
    path('survey/', views.survey, name='survey'),
    path('home/', views.home, name='home'),
    path('homedish/<int:dish_id>/', views.homedish, name='homedish'),
    path('saved/', views.saved, name='saved'),
    path('saveddish/<int:dish_id>/', views.saveddish, name='saveddish'),
    path('cooked/', views.cooked, name='cooked'),
    path('settings/', views.settings, name='settings'),
    path('editprofile/', views.editprofile, name='editprofile'),
    path('mealpref/', views.mealpref, name='mealpref'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),  # Add this line
    path('faqs/', views.faqs, name='faqs'),      # Add this line
    path('terms/', views.terms, name='terms'),  # Add this line
]
