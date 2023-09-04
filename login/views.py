from django.shortcuts import render, redirect
from django import views
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import authenticate, login
from django.urls import reverse
# from editor.forms import SignInForm

from .forms import SignInForm, SignUpForm
from .models import User
from django.contrib.sessions import base_session

class SignInView(views.View):
    template_data = {
        'form': SignInForm,
        'msg': None,
    }

    def get(self, request):
        return render(request, 'login/LogInPage.html', self.template_data)
    
    def post(self, request):
        usr = authenticate(username=request.POST['username'], password=request.POST['password'])
        print(usr)
        if usr:
            request.session['user_id'] = usr.id
            return redirect(reverse("editor:editor index"))
        else:
            self.template_data['msg'] = "No user with such nickname"
        request.session["user"] = None

        return render(request, 'login/LogInPage.html', self.template_data)
    

    
class SignUpView(views.View):
    template_data = {
        "form": SignUpForm,
        "errors_msg": None,
    }

    def get(self, request):
        return render(request, 'login/SignUpPage.html', self.template_data)
    
    def post(self, request):
        form_data = request.POST
        form = SignUpForm(form_data)

        if form.is_valid():
            print("valid")
            form.save()
            usr = User.objects.get(username=form_data['username'])
            request.session['user_id'] = usr.id
            return redirect(reverse('editor:editor index'))

        else:
            self.template_data["form"] = form
            self.template_data['errors_msg'] = form.errors
            print(f"Errors: {form.errors}") 
            return render(request, 'login/SignUpPage.html', self.template_data)



# Create your views here.
def sign_in(request):
    if request.POST:
        print(request.POST)
        usr = User.objects.filter(nickname=request.POST['nickname']).get(password=request.POST['password'])
        if usr:
            print(f"User {usr.nickname} logged in")
            request.session['user_id'] = usr.id
            print(usr)
        else:
            request.session["user"] = None
            return render(request, 'login/LogInPage.html', {'form': SignInForm()})

    else:
        return render(request, 'login/LogInPage.html', {'form': SignInForm()})
    
    return redirect(reverse("editor:editor_index"))

# def sign_up(request):
#     return render(request, 'editor/CreateUser.html', {'form': UserForm()})