from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def profile(request, name):
    return render(request, '/templates/profile.html', {"username": name,})
    return HttpResponse(f"Hello, user {id}")