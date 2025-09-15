from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.shortcuts import render

def home(request):
    return render(request, 'home.html') 

def dashboard(request):
    return render(request, 'dashboard.html')

def notes(request): 
    return render(request, 'notes.html')

def upload_notes(request):
    return render(request, 'upload_notes.html')

def live_projects(request):
    return render(request, 'live_projects.html')

def profile(request):
    return render(request, 'profile.html')

def resume_builder(request):
    return render(request, 'resume_builder.html')

def membership(request):
    return render(request, 'membership.html')
