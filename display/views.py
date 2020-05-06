from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin

class SetDisplay(LoginRequiredMixin, TemplateView):
    template_name = 'display/home.html'

class Scrape(LoginRequiredMixin, TemplateView):
# This function does a post request to the API using the information acquired from the info_scraper function
    template_name = 'display/scrape.html'

def user_login(request):
# Implementation of the custom login
# -----------------------------------------------------------------------------------
# Logs in the user is authenticated and redirects them to the homepage
# else, passes an error messsage as context which is displayed in red in the template
    context = None 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password') 
        auth = authenticate(request, username=username, password=password)

        if auth is not None:
            login(request, auth)
            return redirect('display_home')
        else:
            context= {'errors': 'Authentication failed, try a different username/password combination'}

    return render(request, 'display/login.html', context=context) 


