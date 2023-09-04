from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from novellist.settings import BASE_DIR
import os
from .models import *
from .forms import *
from django.urls import reverse


class CreateAccountView(View):
    def get(self, request):
        return render(request, 'create_account.html', {})
    def post(self, request):
        usr = User(
            nickname=request.POST['nickname'],
            password=request.POST['password'],
        )

class EditorIndexView(View):

    def get(self, request):
        
        try:
            request.session['user_id']
            usr = User.objects.get(id=request.session['user_id'])

            template_data = {
                "user": usr,
                "projects":
                Story.objects.filter(owner=usr.id),
                "len": len(Story.objects.filter(owner=usr.id))
                }
            
            return render(request, 'editor/editor_index_auth.html', template_data)
        except KeyError:
            return redirect(reverse('login:sign in'))
    def post(self, request):
        pass

# Create your views here.
def editor_index(request):
    usr = User.objects.get(id=request.session['user_id'])
    if usr:
        return render(request, 'editor/editor_index_auth.html', {"user": usr, "projects": Story.objects.filter(owner=usr.id), "len": len(Story.objects.filter(owner=usr.id))})
    else:
        return render(request, 'editor/editor_index_unauth.html', {})








def story_editor(request):
    return HttpResponse("Edit the story")

def project_manager(request):
    print(request.GET)
    return HttpResponse("Here you will see all projects, associated with this account")

def nums(request, number_param):
    return HttpResponse(f"<h1>your param is: {number_param}. Enjoy this fact")

def forms(request):
    print(request.POST)
    return render(request, 'editor/forms.html')
    return HttpResponse("<h1>Nothing<h1>")
    